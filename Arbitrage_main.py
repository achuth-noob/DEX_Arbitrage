from test_tokens import *
from address import *
from web3 import Web3
from keys import *
import Sushiswap
import Uniswap
import pandas as pd
import numpy as np
import itertools
import pprint
import json
import os

class Uniswap_nPoolArbitrage_Utils(object):
    """
    Flow of the Arb should be as follows -
        (A,B) -> (B,C) -> .......... (N,A)
    Reserves of the tokens should be arranged in the above order.
    """
    def __init__(self,_df_reserves):
        self.df = _df_reserves
        self.n = int((len(self.df.columns)-1)/2) # last column is f.
        self.f = self.df['f'][0]
        self.rows = len(self.df)
        self.df['b_n'] = self.calculate_b_n()
        self.df['track_b_n'] = np.where(self.df['b_n'] > 0, 1, "NaN")
        self.df.dropna(subset = ["track_b_n"], inplace=True)
        if self.df.empty():
            return
        self.df['a_n'] = self.calculate_a_n()
        self.df['c_n'] = self.calculate_c_n()

    def calculate_a_n(self,n):
        if n == 2:
            return (self.f*self.df[self.df.columns[2]]+self.df[self.df.columns[1]]*self.f**2)
        tmp = pd.DataFrame({"tmp":np.array([1 for i in range(self.rows)])})
        for i in range(1,n):
            tmp["tmp"]*=self.df[self.df.columns[2*i-1]]
        df_n_a = self.calculate_a_n(n-1)*self.df[self.df.columns[2*(n-1)]]+ \
            tmp*self.f**n
        return df_n_a

    def calculate_b_n(self):
        n_b = pd.DataFrame({"tmp1":np.array([1 for i in range(self.rows)])})
        n_b["tmp2"] = np.array([1 for i in range(self.rows)])
        tmp2 = pd.DataFrame({"tmp": np.array([1 for i in range(self.rows)])})
        for i in range(1,self.n+1):
            n_b["tmp1"] *= self.df[self.df.columns[2*i-1]]
        for i in range(self.n):
            n_b["tmp2"] *= self.df[self.df.columns[2*i]]
        n_b["out"] = n_b["tmp1"]*self.f**self.n-n_b["tmp2"]
        return n_b["out"]

    def calculate_c_n(self):
        n_b = pd.DataFrame({"tmp1": np.array([1 for i in range(self.rows)])})
        for i in range(self.n):
            n_b["tmp1"] *= self.df[self.df.columns[2*i]]
        return n_b["tmp1"]

class Uniswap_nPoolArbitrage(object):
    def __init__(self,_exchange_obj_list):
        self.exchanges_list = _exchange_obj_list
        self.n = len(_exchange_obj_list)
        self.token_reserves = {}
        self.main_df = pd.DataFrame({"tokens_comb":np.array(list(itertools.permutations(tokens, 2)),
                                                            dtype=np.dtype('U20,U20'))})
        # print(self.main_df)
        for i in self.exchanges_list:
            tmp1=[]
            tmp2=[]
            k=0
            for j in token_comb:
                try:
                    # DB call
                    [reserve1,reserve2,t] = i.get_exact_reserves(tokens[j[0]],tokens[j[1]])
                    # [self.main_df[f"{i.name}_t0"], self.main_df[f"{i.name}_t1"], t] = \
                    #     i.get_exact_reserves(self.main_df['tokens_comb'][0], self.main_df['tokens_comb'][0])
                    tmp1.append(reserve1)
                    tmp2.append(reserve2)
                except:
                    print(i.name,j[0], j[1])
                    tmp1.append(np.nan)
                    tmp2.append(np.nan)
                    continue
                k+=1
            self.main_df[f"{i.name}_t0"]=tmp1
            self.main_df[f"{i.name}_t1"]=tmp2
        self.main_df.dropna(inplace=True)
        print(self.main_df)

class Direct_Arbitrage(object):
    """
    Direct Arbitrage -
    1. Converts token1 to token2 in exchange 1.
    2. Converts back token2 to token1 in exchange2.
    """
    def __init__(self,_exchange_obj_list):
        self.exchanges_list = _exchange_obj_list
        self.token_reserves = {}
        # DB call
        # token_comb = list(itertools.permutations(tokens, 2))
        # pprint.pprint(token_comb)
        for i in self.exchanges_list:
            tmp = {}
            for j in token_comb:
                try:
                    # DB call
                    [reserve1,reserve2,t] = i.get_exact_reserves(tokens[j[0]],tokens[j[1]])
                    tmp[j[0],j[1]]={j[0]: reserve1,j[1]: reserve2}
                except:
                    continue
            self.token_reserves[i.name]=tmp
        # pprint.pprint(self.token_reserves)

    @staticmethod
    def arbitrage_returns(_reserve1_1,_reserve1_2,_reserve2_1,_reserve2_2):
        a_in_1 = 0.000001
        a_out_1 = Sushiswap.SushiswapUtils.get_amount_out(a_in_1,_reserve1_2,_reserve1_1)
        a_out_2 = Uniswap.UniswapV2Utils.get_amount_out(a_out_1,_reserve2_1,_reserve2_2)
        return ((a_out_2-a_in_1)/a_in_1)*100

    def analysis(self):
        for i in self.token_reserves['sushiswap']:
            for j in self.token_reserves['uniswap']:
                if i==j:
                    reserve1_1=self.token_reserves['sushiswap'][i][i[0]]
                    reserve1_2=self.token_reserves['sushiswap'][i][i[1]]
                    reserve2_1=self.token_reserves['uniswap'][j][j[0]]
                    reserve2_2=self.token_reserves['uniswap'][j][j[1]]
                    print(reserve1_1,reserve1_2,reserve2_1,reserve2_2)
                    arb_ret = self.arbitrage_returns(reserve1_1,reserve1_2,reserve2_1,reserve2_2)
                    print("Arb - ",i,arb_ret,'%')

print("---------------------Process Initialized---------------------")
uniswap_obj = Uniswap.UniswapV2Client(owner_address,owner_private_key,provider)
sushiswap_obj = Sushiswap.SushiswapClient(owner_address,owner_private_key,provider)

# i = 1
# while True:
#     print(f'--------------Iteration {i} stared--------------')
#     Direct_Arbitrage([uniswap_obj,sushiswap_obj]).analysis()
#     i+=1

Uniswap_nPoolArbitrage([uniswap_obj,sushiswap_obj])


