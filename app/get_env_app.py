import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        poll_secs = 300     # same as polling OpenWeather API

    return poll_secs


def get_num_bitcoin():
    """
    Return the number of BTC I own
    :return:
    """
    if 'BITCOIN' in os.environ:
        bitcoin_investment = os.environ['BITCOIN']
    else:
        bitcoin_investment = 0.00057766     # How many bitcoin do I own

    return bitcoin_investment
