from Uniswap import UniswapV2Client,ERC20,UniswapV2Utils
from Sushiswap import SushiswapClient
from tokens import *
from address import *
from web3 import Web3
from keys import *
import itertools
import pprint
import web3
import json
import os

uniswap_obj = UniswapV2Client(owner_address,owner_private_key,provider)
sushiswap_obj = SushiswapClient(owner_address,owner_private_key,provider)
# client = SushiswapClient(owner_address,owner_private_key,provider)

# tokens = {
#     'USDT': {'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7'},
#     'USDC':{'address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'},
#     'UNI':{'address': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'},
#     'WETH':{'address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'},
#     'AAVE': {'address': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9'},
#     'DAI':{'address': '0x6B175474E89094C44Da98b954EedeAC495271d0F'}
# }

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

# connection = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
# # print(connection.isConnected())
# sushifactory_abi = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
#                                                   f"/assests/" + "SushiswapFactory.json")))
# print(type(sushifactory_abi))
# PAIR_ABI = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
#                                           f"/assests/" + "IUniswapV2Pair.json")))['abi']
# contract = connection.eth.contract(
#             address=Web3.toChecksumAddress(sushiswap_factory_address), abi=sushifactory_abi)
# pair_contract = connection.eth.contract(
#             address=Web3.toChecksumAddress(contract.functions.allPairs(1).call()), abi=PAIR_ABI)

# print(contract.functions.getPair(Web3.toChecksumAddress(tokens['USDC']),Web3.toChecksumAddress(tokens['DAI'])).call())
# print(pair_contract.functions.getReserves().call())
# print()
# print(sushiswap_obj.get_reserves(tokens['USDC'], tokens['DAI']))

# provider = 'https://mainnet.infura.io/v3/edab650efa674a98adb0a7b65be35d65'
# def query_token(_provider,_token_addr):
#     connection = Web3(Web3.HTTPProvider(_provider, request_kwargs={"timeout": 60}))
#     # print(connection.isConnected())
#     token_abi = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
#                                                       f"/assests/" + "IUniswapV2ERC20.json")))['abi']
#     try:
#         contract = connection.eth.contract(
#             address=Web3.toChecksumAddress(_token_addr), abi=token_abi)
#         q = contract.functions.decimals().call()
#         return True
#     except:
#         return False
# query_token(provider,tokens['DAI']['address'])

# token_reserves = []
# token_comb = list(itertools.combinations(tokens,2))
# pprint.pprint(token_comb)
# print(token_comb[0][0])
#
# for j in range(len(tokens)):
#     for k in range(j + 1, len(tokens)):
#         if j == k:
#             continue
#         print(tokens[j])
#         try:
#             print('Hi')
#             [reserve1, reserve2, t] = sushiswap_obj.get_reserves(tokens[j].lower(), tokens[k].lower())
#             print(reserve1,reserve2)
#             token_reserves.append({f'{j}':reserve1,f'{k}':reserve2})
#         except:
#             continue
# print(token_reserves)
# for i in tokens:
#     (token0, token1) = UniswapV2Utils.sort_tokens(tokens[i], tokens)
# pprint.pprint(uniswap_obj.get_exact_reserves(tokens['DAI'], tokens['USDC']))
# pprint.pprint(uniswap_obj.get_exact_reserves(tokens['USDC'], tokens['DAI']))

# pairs=json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/precompute_data/UniswapV2Pairs.json" )))
# pprint.pprint(pairs)
# for i in pairs:
#     for j in pairs[i]:
#         print(j)
#         # if j=='address':
#         #     print(i[j])
#     break
# addr = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
# print('address - 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
# print(f'checksum address - {Web3.toChecksumAddress(addr)}')