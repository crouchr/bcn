# https://developers.coinbase.com/api/v2#exchange-rates
# https://www.coindesk.com/coindesk-api

import time

from pprint import pprint
import yaml     # install as PyYaml

import get_env
import get_env_app
import send_metrics_to_telegraf
import blockchaininfo_api
from bitcoin_rpc_client import Bitcoin
import bitnodes_api
import xgminer_api
import coinbase_api
import fear_and_greed_index_api


def get_bcnd_config(bcnd_config_filename):

    with open(bcnd_config_filename) as f:
        bcnd_vars = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    return bcnd_vars

# btc, btc_invested, min_rate, max_rate = get_bcnd_config()


def main():
    version = get_env.get_version()
    verbose = get_env.get_verbose()
    stage = get_env.get_stage()

    telegraf_endpoint_host = get_env_app.get_telegraf_endpoint()    # can be read from ENV
    poll_secs = get_env_app.get_poll_secs()
    bitcoind_host = get_env_app.get_bitcoind_host()
    bitcoind_username = get_env_app.get_bitcoind_username()
    bitcoind_password = get_env_app.get_bitcoind_password()
    bitcoin_miner_host = get_env_app.get_bitcoin_miner_host()

    max_rate = -9999999             # GBP
    min_rate = 999999
    max_rate_usd = -9999999
    min_rate_usd = 999999

    last_rate_usd = None

    if stage == 'PRD':
        bcnd_config_filename = '/data/btc/bcnd.yml'
    else:
        bcnd_config_filename = '../data/btc/bcnd.yml'

    print('bcnd started, version=' + version)
    print('verbose=' + verbose.__str__())
    print('stage=' + stage.__str__())
    print('bcnd_config_filename=' + bcnd_config_filename)
    print('telegraf_endpoint_host=' + telegraf_endpoint_host)
    print('bitcoind_host=' + bitcoind_host.__str__())
    print('bitcoin_miner_host=' + bitcoin_miner_host.__str__())
    print('bitcoind_username=' + bitcoind_username.__str__())
    print('bitcoind_password=' + bitcoind_password.__str__())
    print('poll_secs=' + poll_secs.__str__())

    metric_name = 'bcnd_metrics_v2'
    bitcoin = Bitcoin(bitcoind_username, bitcoind_password, bitcoind_host, 8332)
    last_block_epoch = 0
    last_block_number = 0
    last_block_mine_time_mins = 0

    while True:
        try:
            print('-----')
            print(time.ctime())
            status, blockchain_info = bitcoin.getblockchaininfo()
            if 'result' in blockchain_info:     # if local bitcoind has just been restarted
                time.sleep(240)
                continue

            status, fng_info = fear_and_greed_index_api.get_fng_index()
            if status is True:
                fng_index = fng_info['value']
            else:
                fng_index = -10

            number_of_bitcoin_nodes = bitnodes_api.get_number_bitcoin_nodes()
            if number_of_bitcoin_nodes is None:
                number_of_bitcoin_nodes = -10

            status, mining_info = bitcoin.getmininginfo()

            # mining info
            difficulty = mining_info['difficulty']
            block_number = mining_info['blocks']
            print('block_number=' + block_number.__str__())
            networkhashps = mining_info['networkhashps']
            pooled_tx = mining_info['pooledtx']

            if block_number > last_block_number:
                now = time.time()
                blocks_processed = block_number - last_block_number
                last_block_mine_time_mins = (now - last_block_epoch) / (60.0 * blocks_processed)
                last_block_epoch = now
                last_block_number = block_number
                if last_block_mine_time_mins > 30:
                    last_block_mine_time_mins = 0

            print('blocks_processed=' + blocks_processed.__str__())
            print('last_block_mine_time_mins=' + last_block_mine_time_mins.__str__())
            print('last_block_number=' + last_block_number.__str__())

            # blockchain info
            size_on_disk = blockchain_info['size_on_disk']
            size_on_disk_gbytes = round(size_on_disk / (1024 * 1024 * 1024), 2)

            status, bcn_info = coinbase_api.get_bcn_price()
            if status != 200:
                print('error calling API, sleeping...')
                time.sleep(60)
                continue            # go to start of loop

            bcnd_vars = get_bcnd_config(bcnd_config_filename)
            # btc = float(bcnd_vars['num_btc']) btc = number of richards BTC

            e_wallet_address = bcnd_vars['e_wallet_address']
            a_wallet_address = bcnd_vars['a_wallet_address']
            r_wallet_address = bcnd_vars['r_wallet_address']
            cbase_wallet_address = bcnd_vars['cbase_wallet_address']

            e_btc = blockchaininfo_api.check_balance(e_wallet_address)
            a_btc = blockchaininfo_api.check_balance(a_wallet_address)
            r_btc = blockchaininfo_api.check_balance(r_wallet_address)
            cbase_btc = blockchaininfo_api.check_balance(cbase_wallet_address)

            # gbp_invested = float(bcnd_vars['gbp_invested'])
            # high_alarm = int(bcnd_vars['high_alarm'])
            # low_alarm = int(bcnd_vars['low_alarm'])
            # return_percent_line = int(bcnd_vars['return_percent_line'])

            e_btc_in_gbp = float(e_btc) * bcn_info['GBP']       # what are E BTC worth in GBP
            a_btc_in_gbp = float(a_btc) * bcn_info['GBP']       # what are A BTC worth in GBP
            r_btc_in_gbp = float(r_btc) * bcn_info['GBP']       # what are R BTC worth in GBP
            cbase_btc_in_gbp = float(cbase_btc) * bcn_info['GBP']

            total_btc = e_btc + a_btc + r_btc + cbase_btc
            total_btc_in_gbp = round(total_btc * bcn_info['GBP'], 2)

            if bcn_info['GBP'] < min_rate:
                min_rate = bcn_info['GBP']

            if bcn_info['GBP'] > max_rate:
                max_rate = bcn_info['GBP']

            if bcn_info['USD'] < min_rate_usd:
                min_rate_usd = bcn_info['USD']

            if bcn_info['USD'] > max_rate_usd:
                max_rate_usd = bcn_info['USD']

            if last_rate_usd == None:
                last_rate_usd = bcn_info['USD']

            btc_usd_change = round(bcn_info['USD'] - last_rate_usd, 2)

            # return_percent = round(100 * btc_in_gbp / gbp_invested, 2)

            # My lottery mining rig
            miner_results = xgminer_api.get_miner_summary(bitcoin_miner_host, 4028)
            if miner_results['status'] == True:
                miner_found_blocks = miner_results['found_blocks']
                miner_tstamp = miner_results['tstamp']
                # miner_giga_hps_avg = miner_results['giga_hps_avg']
                miner_giga_hps = miner_results['giga_hps']
                miner_code = miner_results['code']
                miner_hw_errors = miner_results['hw_errors']
                miner_remote_failures = miner_results['remote_failures']
                miner_hashing_online = miner_results['miner_hashing_online']
            else:
                miner_found_blocks = -10
                miner_tstamp = -10
                miner_giga_hps = -10
                miner_code = -10
                miner_hw_errors = -10
                miner_remote_failures = -10
                miner_hashing_online = -10

            # Construct the metric bundle
            metrics = {
                    'metric_name': metric_name,
                    'e_btc': e_btc,
                    'a_btc': a_btc,
                    'r_btc': r_btc,
                    'cbase_btc': cbase_btc,
                    'total_btc': total_btc,
                    'e_btc_worth_gbp': round(e_btc_in_gbp, 2),
                    'a_btc_worth_gbp': round(a_btc_in_gbp, 2),
                    'r_btc_worth_gbp': round(r_btc_in_gbp, 2),
                    'cbase_btc_worth_gbp': round(cbase_btc_in_gbp, 2),
                    'total_btc_worth_gbp': total_btc_in_gbp,
                    'bitcoin_gbp': bcn_info['GBP'],
                    'bitcoin_usd': bcn_info['USD'],
                    'bitcoin_eur': bcn_info['EUR'],
                    'btc_min_rate': min_rate,
                    'btc_max_rate': max_rate,
                    'btc_min_rate_usd': min_rate_usd,
                    'btc_max_rate_usd': max_rate_usd,
                    'btc_usd_change': btc_usd_change,
                    'block_number': block_number,
                    'size_on_disk': size_on_disk,
                    'size_on_disk_gbytes': size_on_disk_gbytes,
                    'difficulty': difficulty,
                    'pooledtx': pooled_tx,
                    'networkhash': networkhashps,
                    'num_btc_nodes': number_of_bitcoin_nodes,
                    'miner_found_blocks': miner_found_blocks,
                    'miner_tstamp': miner_tstamp,
                    'miner_giga_hps': miner_giga_hps,
                    'miner_code': miner_code,
                    'miner_hw_errors': miner_hw_errors,
                    'miner_remote_failures': miner_remote_failures,
                    'miner_hashing_online': miner_hashing_online,
                    'fng_index': fng_index
            }

            pprint(metrics)

            send_metrics_to_telegraf.send_metrics(telegraf_endpoint_host, metrics, verbose)

            last_rate_usd = bcn_info['USD']

            time.sleep(poll_secs)

        except Exception as e:
            print('main() : Error : ' + e.__str__())
            print('sleeping...')
            # beep.warning(num_beeps=2, sound=3)
            time.sleep(180)     # wait 3 mins
            continue


if __name__ == '__main__':
    main()
