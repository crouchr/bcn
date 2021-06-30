import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        # poll_secs = 120
        poll_secs = 300

    return poll_secs


def get_telegraf_endpoint():
    if 'TELEGRAF_ENDPOINT' in os.environ:
        telegraf_endpoint = os.environ['TELEGRAF_ENDPOINT']
    else:
        telegraf_endpoint = '192.168.1.180'

    return telegraf_endpoint


def get_db_hostname():
    if 'SQL_DB_HOSTNAME' in os.environ:
        hostname = os.environ['SQL_DB_HOSTNAME']
    else:
        hostname = '192.168.1.5'            # Use Test MySQL on Dev workstation
        # hostname = '192.168.1.180'        # Use production MySQL

    return hostname


def get_bitcoind_username():
    if 'BITCOIND_USERNAME' in os.environ:
        bitcoind_username = os.environ['BITCOIND_USERNAME']
    else:
        bitcoind_username = 'bitcoinrpc'

    return bitcoind_username


def get_bitcoind_password():
    if 'BITCOIND_PASSWORD' in os.environ:
        bitcoind_password = os.environ['BITCOIND_PASSWORD']
    else:
        bitcoind_password = 'protectrpcserver1928'

    return bitcoind_password


def get_bitcoind_host():
    if 'BITCOIND_HOST' in os.environ:
        bitcoind_host = os.environ['BITCOIND_HOST']
    else:
        bitcoind_host = 'j1900'

    return bitcoind_host