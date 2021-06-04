import os
import json
from tokens import *
import Sushiswap
from keys import *
import Uniswap

uniswap_obj = Uniswap.UniswapV2Client(owner_address,owner_private_key,provider)
sushiswap_obj = Sushiswap.SushiswapClient(owner_address,owner_private_key,provider)

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

simArbObj = Simple_arbitrage(tokens['USDT'],tokens['USDC'])
simArbObj.search_arbitrage()