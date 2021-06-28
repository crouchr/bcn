# https://developers.coinbase.com/api/v2#exchange-rates
# https://www.coindesk.com/coindesk-api

import time
import requests
import json
from pprint import pprint
import yaml     # install as PyYaml

import get_env
import get_env_app
import send_metrics_to_telegraf
import get_wallet_balance


def get_bcnd_config(bcnd_config_filename):

    with open(bcnd_config_filename) as f:
        bcnd_vars = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    return bcnd_vars

# btc, btc_invested, min_rate, max_rate = get_bcnd_config()


def get_bcn_price():
    """
    Call REST API endpoint to get current BTC price

    :param endpoint:e.g. 'http://127.0.0.1:9500/wind_deg_to_wind_rose'
    :param query: e.g. query = {'wind_deg': wind_deg}
    :return:
    """
    try:
        bcn_info = {}
        endpoint = 'https://api.coindesk.com/v1/bpi/currentprice.json'

        response = requests.get(endpoint,)

        if response.status_code != 200:
            return 500, None

        response_dict = json.loads(response.content.decode('utf-8'))

        bcn_info['updateduk'] = response_dict['time']['updateduk']
        bcn_info['GBP'] = response_dict['bpi']['GBP']['rate_float']
        bcn_info['USD'] = response_dict['bpi']['USD']['rate_float']
        bcn_info['EUR'] = response_dict['bpi']['EUR']['rate_float']

        return response.status_code, bcn_info

    except Exception as e:
        print('get_bcn_price() : Error=' + e.__str__())
        return 500, None


def main():
    version = get_env.get_version()
    verbose = get_env.get_verbose()
    stage = get_env.get_stage()

    telegraf_endpoint_host = get_env_app.get_telegraf_endpoint()    # can be read from ENV

    poll_secs = get_env_app.get_poll_secs()
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
    print('poll_secs=' + poll_secs.__str__())

    metric_name = 'bcnd_metrics_v2'

    while True:
        try:
            status, bcn_info = get_bcn_price()
            if status != 200:
                print('error calling API, sleeping...')
                time.sleep(60)
                continue            # go to start of loop

            bcnd_vars = get_bcnd_config(bcnd_config_filename)
            # btc = float(bcnd_vars['num_btc']) btc = number of richards BTC

            e_wallet_address = bcnd_vars['e_wallet_address']
            a_wallet_address = bcnd_vars['a_wallet_address']
            r_wallet_address = bcnd_vars['r_wallet_address']
            e_btc = get_wallet_balance.check_balance(e_wallet_address)
            a_btc = get_wallet_balance.check_balance(a_wallet_address)
            r_btc = get_wallet_balance.check_balance(r_wallet_address)

            # gbp_invested = float(bcnd_vars['gbp_invested'])
            # high_alarm = int(bcnd_vars['high_alarm'])
            # low_alarm = int(bcnd_vars['low_alarm'])
            # return_percent_line = int(bcnd_vars['return_percent_line'])

            e_btc_in_gbp = float(e_btc) * bcn_info['GBP']       # what are E BTC worth in GBP
            a_btc_in_gbp = float(a_btc) * bcn_info['GBP']       # what are A BTC worth in GBP
            r_btc_in_gbp = float(r_btc) * bcn_info['GBP']       # what are R BTC worth in GBP
            total_btc = e_btc + a_btc + r_btc
            total_btc_in_gbp = total_btc * bcn_info['GBP']

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

            # print(time.ctime() + \
            #       ' (updated at ' + bcn_info['updateduk'] + ')' + \
            #       ' : BTC rate (GBP) = ' + bcn_info['GBP'].__str__() + \
            #       ', E_BTC = ' + e_btc.__str__() + \
            #       ', A_BTC = ' + a_btc.__str__() + \
            #       ', R_BTC = ' + r_btc.__str__() + \
            #       ', BTC invested = £' + round(gbp_invested, 2).__str__() + \
            #       ' : => GBP value = £' + round(btc_in_gbp, 2).__str__()
            #       )

            # Construct the metric bundle
            metrics = {
                    'metric_name': metric_name,
                    'e_btc': e_btc,
                    'a_btc': a_btc,
                    'r_btc': r_btc,
                    'total_btc': total_btc,
                    'e_btc_worth_gbp': e_btc_in_gbp,
                    'a_btc_worth_gbp': a_btc_in_gbp,
                    'r_btc_worth_gbp': r_btc_in_gbp,
                    'total_btc_worth_gbp': total_btc_in_gbp,
                    'bitcoin_gbp': bcn_info['GBP'],
                    'bitcoin_usd': bcn_info['USD'],
                    'bitcoin_eur': bcn_info['EUR'],
                    'btc_min_rate': min_rate,
                    'btc_max_rate': max_rate,
                    'btc_min_rate_usd': min_rate_usd,
                    'btc_max_rate_usd': max_rate_usd,
                    'btc_usd_change': btc_usd_change
            }

            pprint(metrics)

            # send_metrics_to_telegraf.send_metrics(telegraf_endpoint_host, metrics, verbose)

            last_rate_usd = bcn_info['USD']

            time.sleep(poll_secs)

        except Exception as e:
            print('main() : Error : ' + e.__str__())
            print('sleeping...')
            # beep.warning(num_beeps=2, sound=3)
            time.sleep(180)     # wait 3 mins
            continue


if __name__ == '__main__' :
    main()
