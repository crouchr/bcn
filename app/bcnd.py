# https://developers.coinbase.com/api/v2#exchange-rates
# https://www.coindesk.com/coindesk-api

import time
import requests
import json
from pprint import pprint

import get_env
import get_env_app
import send_metrics_to_telegraf


def get_bcn_price():
    """
    Call REST API endpoint

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

        return response.status_code, bcn_info

    except Exception as e:
        print('get_bcn_price() : Error=' + e.__str__())
        return 500, None


def main():
    version = get_env.get_version()
    verbose = get_env.get_verbose()
    btc = get_env_app.get_num_bitcoin()
    telegraf_endpoint_host = get_env.get_telegraf_endpoint()    # can be read from ENV

    poll_secs = get_env_app.get_poll_secs()

    print('bcnd started, version=' + version)
    print('verbose=' + verbose.__str__())
    print('telegraf_endpoint_host=' + telegraf_endpoint_host)
    print('poll_secs=' + poll_secs.__str__())

    metric_name = 'bcnd_metrics'

    while True:
        try:
            status, bcn_info = get_bcn_price()
            btc_in_gbp = float(btc) * bcn_info['GBP']      # what are my BTC worth in GBP

            print(time.ctime() +\
                  ' (updated at ' + bcn_info['updateduk'] + ')' + \
                  ' : BTC rate (GBP) = ' + bcn_info['GBP'].__str__() +\
                  ', BTC = ' + btc.__str__() +\
                  ', GBP value = £' + round(btc_in_gbp, 2).__str__()
                  )

            # Construct the metric bundle
            metrics = {
                    'metric_name': metric_name,
                    'btc': btc,
                    'btc_worth_gbp': btc_in_gbp,
                    'bitcoin_gbp': bcn_info['GBP']
            }

            send_metrics_to_telegraf.send_metrics(telegraf_endpoint_host, metrics, verbose)

            time.sleep(poll_secs)

        except Exception as e:
            print('Error : ' + e.__str__())
            print('sleeping...')
            # beep.warning(num_beeps=2, sound=3)
            time.sleep(180)     # wait 3 mins
            continue


if __name__ == '__main__' :
    main()
