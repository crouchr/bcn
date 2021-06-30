
import requests
import json
import time


def get_number_bitcoin_nodes():
    """
    Call REST API endpoint

    :return:
    """
    try:
        endpoint = 'https://bitnodes.io/api/v1/snapshots/latest/'
        response = requests.get(endpoint,)

        if response.status_code != 200:
            return None

        response_dict = json.loads(response.content.decode('utf-8'))
        # pprint(response_dict)

        number_of_nodes = response_dict['total_nodes']

        return number_of_nodes

    except Exception as e:
        print('get_number_bitcoin_nodes : Error=' + e.__str__())
        return None


if __name__ == '__main__':
    while True:
        nodes = get_number_bitcoin_nodes()
        print('number of bitcoin nodes=' + nodes.__str__())
        print('sleeping...')
        time.sleep(10)
