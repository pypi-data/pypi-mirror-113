from web3 import Web3
import requests as requests
import matplotlib.pyplot as plt
from dateutil import parser

class LiquidityPools:
    def __init__(self,rpc_url='https://backend.sovryn.app/rpc',contract_address=None):
        self.__rpc_url = rpc_url
        self.__address = contract_address
    def lp_get(self):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post('https://backend.sovryn.app/rpc',json={"method":"custom_getLoanTokenHistory","params":[{"address":self.__address}]},headers=headers)
        return result.json()
    def print(self):
        result = self.lp_get()
        for r in result:
            print(r)
    def chart(self):
        result = self.lp_get()
        supply = []
        supply_apr = []
        borrow_apr = []
        timestamp = []
        for r in result:
            supply.append(int(r['supply']) / 100000000)
            supply_apr.append(int(r['supply_apr']) / 10000000000)
            timestamp.append(parser.isoparse(r['timestamp']))
        plt.plot(timestamp,supply_apr)
        plt.show()
 
class RSKNode:
    def __init__(self,url='https://public-node.rsk.co'):
        self.__w3 = Web3(Web3.HTTPProvider('https://public-node.rsk.co'))
    def current_block(self):
        return self.__w3.eth.block_number

