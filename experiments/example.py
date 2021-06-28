# from bitcoincli import Bitcoin
from bitcoin_rpc_client import Bitcoin
import time
from pprint import pprint

host = "j1900"
port = "8332"

username = "bitcoinrpc"
password = "protectrpcserver1928"

bitcoin = Bitcoin(username, password, host, port)

while True:
    print(time.ctime())
    blockchain_info = bitcoin.getblockchaininfo()
    mining_info = bitcoin.getmininginfo()
    # pprint(mining_info)

    # Error handling
    if 'result' in blockchain_info:
        pprint(blockchain_info)
        time.sleep(30)
        continue

    # mining info
    difficulty = mining_info['difficulty']
    blocks = mining_info['blocks']
    networkhashps = mining_info['networkhashps']
    pooledtx = mining_info['pooledtx']

    # blockchain info
    size_on_disk = blockchain_info['size_on_disk']

    pprint(blockchain_info)
    pprint(mining_info)

    time.sleep(30)