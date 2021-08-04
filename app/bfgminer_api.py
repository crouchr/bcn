# Copyright 2013 Christian Berendt
# Copyright 2013 Luke Dashjr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.  See COPYING for more details.

# Move this into an artifact

# original was Python 2 -> I converted it to Python 3
# https://github.com/luke-jr/bfgminer/blob/bfgminer/README.RPC


import logging
import socket
from pprint import pprint


def get_coin_data(hostname, port):
    results = {}

    raw_results = send_command(hostname, port, 'coin', '')
    results['status'] = raw_results['status']
    results['err_msg'] = raw_results['err_msg']
    if raw_results['status'] is False:
        return results

    results['code'] = int(raw_results['Code'])
    results['miner_sw_version'] = raw_results['Description'].replace('}]', '')
    results['tstamp'] = int(raw_results['When'])
    results['current_block_hash'] = raw_results['Current Block Hash']
    results['current_block_time'] = raw_results['Current Block Time']
    results['network_difficulty'] = raw_results['Network Difficulty']

    return results


# G T P E
def get_miner_summary(hostname, port):
    '''

    :param hostname:
    :param port:
    :return:
    '''

    results = {}

    raw_results = send_command(hostname, port, 'summary', '')
    results['status'] = raw_results['status']
    results['err_msg'] = raw_results['err_msg']
    if raw_results['status'] is False:
        return results

    results['code'] = int(raw_results['Code'])
    results['miner_sw_version'] = raw_results['Description'].replace('}]', '')
    results['tstamp'] = int(raw_results['When'])
    results['found_blocks'] = int(raw_results['Found Blocks'])
    results['giga_hps_avg'] = round(float(raw_results['MHS av']) / 1000, 2)
    # results['total_exa_hps'] = round(float(raw_results['Total MH']) / 1000000000, 3)
    results['hw_errors'] = int(raw_results['Hardware Errors'])
    results['remote_failures'] = int(raw_results['Remote Failures'])
    results['network_blocks'] = int(raw_results['Network Blocks'])
    results['get_failures'] = int(raw_results['Get Failures'])
    results['accepted'] = int(raw_results['Accepted'])
    results['rejected'] = int(raw_results['Rejected'])
    results['discarded'] = int(raw_results['Discarded'])

    return results


def send_command(hostname, port, command, parameter):
    '''
    Send raw command to bfgminer and get a dict of results
    :param hostname:
    :param port:
    :param command:
    :param parameter:
    :return:
    '''

    results = {}
    results['status'] = False
    results['err_msg'] = 'Internal error'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((hostname, port))
    except socket.error as e:
        logging.error(e)
        results['status'] = False
        results['err_msg'] = e.__str__()
        return results
    try:
        message_str = "{\"command\" : \"%s\", \"parameter\" : \"%s\"}" % (command, parameter)
        s.send(message_str.encode('utf-8'))
    except socket.error as e:
        logging.error(e)

    data = ''
    while True:
        try:
            newdata = s.recv(1024)
            if newdata:
                data += newdata.__str__()
            else:
                break
        except socket.error as e:
            break

    try:
        s.close()
    except socket.error as e:
        logging.error(e)

    if data:
        results['status'] = True
        results['err_msg'] = None
        fields = data.split(',')
        for field in fields:
            if 'STATUS' in field:
                continue
            key = field.split(':')[0]
            key = key.replace('"', '')
            value = field.split(':')[1]
            value = value.replace('"', '')
            results[key] = value

    print()
    return results


if __name__ == '__main__':
    hostname = 'j1900'
    bfgminer_api_port = 4028

    miner_results = get_miner_summary(hostname, bfgminer_api_port)
    coin_results = get_coin_data(hostname, bfgminer_api_port)

    pprint(miner_results)
    pprint(coin_results)
