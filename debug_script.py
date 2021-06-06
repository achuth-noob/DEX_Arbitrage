from Uniswap import UniswapV2Client,ERC20
from Sushiswap import SushiswapClient
from tokens import *
from address import *
from web3 import Web3
from keys import *
import pprint
import json
import os

sushiswap_obj = SushiswapClient(owner_address,owner_private_key,provider)
# client = SushiswapClient(owner_address,owner_private_key,provider)
#
tokens = {
    'USDT':'0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'USDC':'0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'UNI':'0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
    'WETH':'0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    'AAVE':'0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
    'DAI':'0x6B175474E89094C44Da98b954EedeAC495271d0F'
}
#
# t1 = 'USDC'
# t2 = 'USDT'
# ta = tokens[t1]
# tb = tokens[t2]
# erca = ERC20(ta,owner_address,owner_private_key,provider)
# ercb = ERC20(tb,owner_address,owner_private_key,provider)
#
# pair = client.get_pair(ta,tb)
# # print(type(pair))
#
# [ra,rb,t] = client.get_reserves(ta,tb)
# print('Pair address - ',pair)
# print(f'Uniswap Reserve of {t1},{t2} is {ra}, {rb}')
# print(f'Uniswap Price of {t1}/{t2} is ${ra/rb}')
# print(f'Decimals of {t1} and {t2} are {erca.get_decimal()} and {ercb.get_decimal()}')

connection = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
print(connection.isConnected())
sushifactory_abi = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
                                                  f"/assests/" + "SushiswapFactory.json")))
PAIR_ABI = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
                                          f"/assests/" + "IUniswapV2Pair.json")))['abi']
contract = connection.eth.contract(
            address=Web3.toChecksumAddress(sushiswap_factory_address), abi=sushifactory_abi)
pair_contract = connection.eth.contract(
            address=Web3.toChecksumAddress(contract.functions.allPairs(1).call()), abi=PAIR_ABI)
print(contract.functions.getPair(Web3.toChecksumAddress(tokens['USDC']),Web3.toChecksumAddress(tokens['DAI'])).call())
print(pair_contract.functions.getReserves().call())
print()
print(sushiswap_obj.get_reserves(tokens['USDC'], tokens['DAI']))
print(contract.functions.getPair(tokens['USDC'], tokens['DAI'])).call()