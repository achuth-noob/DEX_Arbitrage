from Uniswap import UniswapV2Client,ERC20,UniswapV2Utils
from Sushiswap import SushiswapClient
from tokens import *
from address import *
from web3 import Web3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keys import *
import itertools
import pprint
import web3
import time
import json
import os

uniswap_obj = UniswapV2Client(owner_address,owner_private_key,provider)
# sushiswap_obj = SushiswapClient(owner_address,owner_private_key,provider)
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
# print(connection.isConnected())
# sushifactory_abi = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
#                                                   f"/assests/" + "SushiswapFactory.json")))
# print(type(sushifactory_abi))
# PAIR_ABI = json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}"
#                                           f"/assests/" + "IUniswapV2Pair.json")))['abi']
# contract = connection.eth.contract(
#             address=Web3.toChecksumAddress(sushiswap_factory_address), abi=sushifactory_abi)
# pair_contract = connection.eth.contract(
#             address=Web3.toChecksumAddress(contract.functions.allPairs(1).call()), abi=PAIR_ABI)
#
# print(contract.functions.getPair(Web3.toChecksumAddress(tokens['USDC']),Web3.toChecksumAddress(tokens['DAI'])).call())
# print(pair_contract.functions.getReserves().call())
# print()
print(uniswap_obj.get_reserves(tokens['YFI'], tokens['UNI']))
print(uniswap_obj.get_reserves(tokens['UNI'], tokens['YFI']))

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

# pairs=json.load(open(os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/data/UniswapV2Pairs.json" )))
# pprint.pprint(pairs)
# for i in pairs:
#     for j in pairs[i]:
#         print(j)
#         # if j=='address':
#         #     print(i[j])
#     break
# addr = '0xeb58343b36c7528f23caae63a150240241310049'
# print('address - 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
# print(f'checksum address - {Web3.toChecksumAddress(addr)}')

# 47594.119296 47880.34725932539 6797585.802299 6797170.7099949075
# 119412910.79666261 49388.46190264566 40977070.60285978 17092.38729813612
# 47901.410192 47577.87558454239 6765625.16264 6771031.976269203
# 236402316.073012 99644.62573142888 123712234.656438 52171.23147589405

#---------------4 Variants possible for direct arb----------------

# ra_1=119412910.79666261
# ra_2=49388.46190264566
# rb_1=40977070.60285978
# rb_2=17092.38729813612
# f1 = 0.997
# f2 = 0.997
# a = rb_1*f1 + rb_2
# b = ra_2*rb_1*f1*f2-ra_1*rb_2
# c = ra_1*rb_2
# print(a,b,c)
# x_opt_in = b/(a*b+a*c+a)
# print(x_opt_in)
#
# if b>0:
#     equation = f'(-{a}*x**2+{b}*x)/({a}*x+{c})'
# elif b == 0:
#     equation = f'(-{a}*x**2)/({a}*x+{c})'
# else:
#     b*=-1
#     equation = f'(-{a}*x**2-{b}*x)/({a}*x+{c})'
# def graph(formula, x_range):
#     x = np.array(x_range)
#     y = eval(formula)
#     print(y)
#     print(formula)
#     plt.plot(x, y)
#     plt.show()
#
# graph(equation,(-10,10))

# uniswap_obj = UniswapV2Client(owner_address, owner_private_key, provider)
#
# conn = Web3(Web3.HTTPProvider(provider))
#
# BATCH_SIZE = 100
#
# QUERY_ABI = json.load(open("./assests/" + "IUniswapV2Query.json"))
# query_contract = conn.eth.contract(address=Web3.toChecksumAddress(uniswap_query_address), abi=QUERY_ABI)
#
# FACTORY_ABI = json.load(open("./assests/" + "IUniswapV2Factory.json"))["abi"]
# uniswap_factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(uniswap_factory_address),
#                                              abi=FACTORY_ABI)
# sushiswap_factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(sushiswap_factory_address),
#                                                abi=FACTORY_ABI)
#
#
# def get_pool_addresses(factory_address):
#     factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(factory_address), abi=FACTORY_ABI)
#     total_number_of_pools = factory_contract.functions.allPairsLength().call()
#     n_batches = int(total_number_of_pools / BATCH_SIZE)
#     pool_addresses = []
#     t_in = time.time()
#     for i in range(n_batches):
#         pool_addresses += query_contract.functions.getPairsByIndexRange(factory_address, i * BATCH_SIZE,
#                                                                         (i + 1) * BATCH_SIZE).call()
#         t_out = time.time()
#         print(f'Time elapsed - {t_out-t_in}s')
#         t_in = t_out
#     pool_addresses += query_contract.functions.getPairsByIndexRange(factory_address, n_batches * BATCH_SIZE,
#                                                                     total_number_of_pools).call()
#     return pool_addresses
#
# get_pool_addresses(uniswap_factory_address)
# obj = np.dtype('U20,U20')
# df = pd.DataFrame({"a": np.array([('USDC', 'DAI'), ('USDC', 'UNI')],dtype=np.dtype('U20,U20'))})
# print(df['a'])


