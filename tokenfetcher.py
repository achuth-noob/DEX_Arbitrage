from web3 import Web3
import json, os
from timeit import default_timer as timer
from address import pair_contract_list
from multicall import Call, Multicall


provider = 'https://mainnet.infura.io/v3/edab650efa674a98adb0a7b65be35d65'
connection = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
# w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/edab650efa674a98adb0a7b65be35d65'))


def query_reserves(_provider):
    connection = Web3(Web3.HTTPProvider(_provider, request_kwargs={"timeout": 60}))

    calls = []
    for i, contract in enumerate(pair_contract_list):
        calls.append(
            Call(contract, ['getReserves()((uint112,uint112,uint32))'], [[f'reserves{i}', from_r]])
        )
    multi = Multicall(calls, _w3=connection)
    print(multi())
    return True

def from_r(value):
    return {'reserve': value}


print(query_reserves(provider))

