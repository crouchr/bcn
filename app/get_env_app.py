import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        poll_secs = 300     # same as polling OpenWeather API
        poll_secs = 60  # same as polling OpenWeather API

    return poll_secs


# def get_num_bitcoin():
#     """
#     Return the number of BTC I own
#     :return:
#     """
#     if 'BITCOIN' in os.environ:
#         bitcoin_investment = os.environ['BITCOIN']
#     else:
#         bitcoin_investment = 0.00057766     # How many bitcoin do I own
#
#     return bitcoin_investment


# def get_gbp_invested():
#     """
#     Return the number of GBP I have put into BTC
#     :return:
#     """
#     if 'GBP_INVESTED' in os.environ:
#         bitcoin_invested = os.environ['GBP_INVESTED']
#     else:
#         bitcoin_invested = 48.51        # How many bitcoin do I own
#
#     return bitcoin_invested
