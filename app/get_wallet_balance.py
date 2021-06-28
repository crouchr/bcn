# Based and improved implementation, inspired by: github.com/circulosmeos/bitcoin-in-tiny-pieces/blob/master/bitcoin-get-address-balance.py
# Developed by: ~geniusprodigy

# FIXME : Make this an artifact

import re
from time import sleep

from urllib.request import urlopen


# FIXME : Fix the exception handling - i.e. do not use exit()
def check_balance(btc_address):
    """
    Return the final balance number of BTC in the wallet address

    :param btc_address:
    :return:
    """

    blockchain_tags_json = [
        'total_received',
        'final_balance',
    ]

    SATOSHIS_PER_BTC = 1e+8

    check_address = btc_address

    parse_address_structure = re.match(r' *([a-zA-Z1-9]{1,34})', check_address)
    if (parse_address_structure is not None):
        check_address = parse_address_structure.group(1)
    else:
        print("This Bitcoin Address is invalid" + check_address)
        return None

    # Read info from Blockchain about the Address
    reading_state = 1
    while (reading_state):
        try:
            htmlfile = urlopen("https://blockchain.info/address/%s?format=json" % check_address, timeout=10)
            htmltext = htmlfile.read().decode('utf-8')
            reading_state = 0
        except:
            reading_state += 1
            print("Checking... " + str(reading_state))
            sleep(60 * reading_state)

    # print("\nBitcoin Address = " + check_address)

    blockchain_info_array = []
    tag = ''
    try:
        for tag in blockchain_tags_json:
            blockchain_info_array.append(
                float(re.search(r'%s":(\d+),' % tag, htmltext).group(1)))
    except:
        print("Error '%s'." % tag);
        return None

    for i, btc_tokens in enumerate(blockchain_info_array):

        # sys.stdout.write("%s \t= " % blockchain_tags_json[i])
        if btc_tokens > 0.0:
            # print("%.8f Bitcoin" % (btc_tokens / SATOSHIS_PER_BTC));
            btc = (btc_tokens / SATOSHIS_PER_BTC)
        else:
            btc = 0.0
            # print("0 Bitcoin");

    return btc


# Test harness
def main():
    test_address = '1FrRd4iZRMU8i2Pbffzkac5u4KwUptmc7S'     # has 0 BTC
    invalid_address = '123A4'
    e_wallet_address = '1LiQTXcXK9ccNG9cC2YBYiad5AsM9RuNE5'
    a_wallet_address = '13V9NsiTwKDboqXtu7obv2vjtEMtnMs4AQ'
    r_wallet_address = '19HvidH9wno6HtZg5JTNEqH6QuiFYjU2zp'

    wallets = [r_wallet_address, a_wallet_address, e_wallet_address, test_address]
    for wallet_address in wallets:
        print('-------------------')
        btc = check_balance(wallet_address)
        print(wallet_address)
        print(btc)


if __name__ == '__main__':
    main()
