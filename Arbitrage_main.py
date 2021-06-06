from tokens import *
from address import *
from web3 import Web3
from keys import *
import Sushiswap
import Uniswap
import pandas as pd
import itertools
import pprint
import json
import os

uniswap_obj = Uniswap.UniswapV2Client(owner_address,owner_private_key,provider)
sushiswap_obj = Sushiswap.SushiswapClient(owner_address,owner_private_key,provider)

<<<<<<< HEAD
# class Simple_arbitrage(object):
#
#     def __init__(self,_token1_addr,_token2_addr):
#         self.flag = True
#         self.token1_addr = _token1_addr
#         self.token2_addr = _token2_addr
#         try:
#             self.pair1_addr = uniswap_obj.get_pair(self.token2_addr,self.token2_addr)
#             self.pair2_addr = sushiswap_obj.get_pair(self.token1_addr,self.token2_addr)
#         except:
#             print('Pair doesnt exist in one of the exchange or both exchanges')
#             self.flag = False
#
#     def search_arbitrage(self):
#         if self.flag == True:
#             [reserve1_1,reserve2_1,t1] = uniswap_obj.get_reserves(self.token1_addr,self.token2_addr)
#             print(reserve1_1,reserve2_1)
#             [reserve2_2,reserve1_2,t2] = sushiswap_obj.get_reserves(self.token2_addr,self.token1_addr)
#             print(f'Reserve Ratios of UNI/SUSHI : {reserve1_1/reserve1_2} and {reserve2_1/reserve2_2}')
#         else:
#             pass
#
#     def simple_arb(self):
#

class Direct_Arbitrage(object):
    """
    Direct Arbitrage -
    1. Converts token1 to token2 in exchange 1.
    2. Converts back token2 to token1 in exchange2.
    """
    def __init__(self,_exchange_obj_list):
        self.exchanges_list = _exchange_obj_list
        self.token_reserves = []
        for i in self.exchanges_list:
            tmp = {}
            token_comb = list(itertools.combinations(tokens, 2))
            for j in token_comb:
                try:
                    [reserve1,reserve2,t] = i.get_reserves(tokens[j[0]],tokens[j[1]])
                    tmp[j[0],j[1]]={j[0]: reserve1,j[1]: reserve2}
                except:
                    continue
            self.token_reserves.append({i.name:tmp})
        pprint.pprint(self.token_reserves)

    # def analysis(self):
    #     for i in self.token_reserves['sushiswap']:
    #         if j in self.token_reserves['uniswap']:


Direct_Arbitrage([uniswap_obj,sushiswap_obj])

    # def normalize_token_reserves(self,token):


    # def search_arbitrage(self):


# simArbObj = Direct_Arbitrage(tokens['UNI'],tokens['DAI'])
# simArbObj.search_arbitrage()
=======
class Simple_arbitrage(object):

    def __init__(self,_token1_addr,_token2_addr):
        self.flag = True
        self.token1_addr = _token1_addr
        self.token2_addr = _token2_addr
        try:
            self.pair1_aadr = uniswap_obj.get_pair(self.token2_addr,self.token2_addr)
            self.pair2_addr = sushiswap_obj.get_pair(self.token1_addr,self.token2_addr)
        except:
            print('Pair doesnt exist in one of the exchange or both exchanges')
            self.flag = False

    def search_arbitrage(self):
        if self.flag == True:
            [reserve1_1,reserve2_1,t1] = uniswap_obj.get_reserves(self.token1_addr,self.token2_addr)
            print(reserve1_1,reserve2_1)
            [reserve2_2,reserve1_2,t2] = sushiswap_obj.get_reserves(self.token2_addr,self.token1_addr)
            print(f'Reserve Ratios of UNI/SUSHI : {reserve1_1/reserve1_2} and {reserve2_1/reserve2_2}')
        else:
            pass

simArbObj = Simple_arbitrage(tokens['USDT']['address'],tokens['USDC']['address'])
simArbObj.search_arbitrage()
>>>>>>> refs/remotes/origin/main
