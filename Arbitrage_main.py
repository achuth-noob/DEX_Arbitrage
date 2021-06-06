from test_tokens import *
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

class Direct_Arbitrage(object):
    """
    Direct Arbitrage -
    1. Converts token1 to token2 in exchange 1.
    2. Converts back token2 to token1 in exchange2.
    """
    def __init__(self,_exchange_obj_list):
        print("---------------------Process Initialized------------------")
        self.exchanges_list = _exchange_obj_list
        self.token_reserves = {}
        token_comb = list(itertools.combinations(tokens, 2))
        pprint.pprint(token_comb)
        for i in self.exchanges_list:
            tmp = {}
            print(i)
            for j in token_comb:
                try:
                    [reserve1,reserve2,t] = i.get_reserves(tokens[j[0]]['address'],tokens[j[1]]['address'])
                    tmp[j[0],j[1]]={j[0]: reserve1,j[1]: reserve2}
                except:
                    continue
            self.token_reserves[i.name]=tmp
        pprint.pprint(self.token_reserves)

    @staticmethod
    def arbitrage_returns(_reserve1_1,_reserve1_2,_reserve2_1,_reserve2_2):
        a_in_1 = 1
        a_in_2 = 1
        a_out_1 = Sushiswap.SushiswapUtils.get_amount_out(a_in_1,_reserve1_1,_reserve1_2)
        a_out_2 = Uniswap.UniswapV2Utils.get_amount_out(a_in_2,_reserve2_1,_reserve2_2)
        return (a_out_1*a_out_2-1)*100

    def analysis(self):
        for i in self.token_reserves['sushiswap']:
            for j in self.token_reserves['uniswap']:
                if i==j:
                    print("Main section running..............")
                    reserve1_1=self.token_reserves['sushiswap'][i][i[0]]
                    reserve1_2=self.token_reserves['sushiswap'][i][i[1]]
                    reserve2_1=self.token_reserves['uniswap'][j][j[0]]
                    reserve2_2=self.token_reserves['uniswap'][j][j[1]]

                    arb_ret = self.arbitrage_returns(reserve1_1,reserve1_2,reserve2_1,reserve2_2)
                    print("Arb - ",i,arb_ret)


Direct_Arbitrage([uniswap_obj,sushiswap_obj]).analysis()


