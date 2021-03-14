import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        poll_secs = 300     # same as polling OpenWeather API

    return poll_secs


