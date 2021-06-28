import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        poll_secs = 300     # same as polling OpenWeather API

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
