import json
from keys import *
from web3 import Web3
import address
import Uniswap, Sushiswap
import numpy as np

uniswap_obj = Uniswap.UniswapV2Client(owner_address, owner_private_key, provider)

conn = Web3(Web3.HTTPProvider(provider))

BATCH_SIZE = 500

QUERY_ABI = json.load(open("assets/" + "IUniswapV2Query.json"))
query_contract = conn.eth.contract(address=Web3.toChecksumAddress(address.uniswap_query_address), abi=QUERY_ABI)

FACTORY_ABI = json.load(open("assets/" + "IUniswapV2Factory.json"))["abi"]
uniswap_factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(address.uniswap_factory_address),
                                             abi=FACTORY_ABI)
sushiswap_factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(address.sushiswap_factory_address),
                                               abi=FACTORY_ABI)


def get_pool_addresses(factory_address):
    factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(factory_address), abi=FACTORY_ABI)
    total_number_of_pools = factory_contract.functions.allPairsLength().call()
    n_batches = int(total_number_of_pools / BATCH_SIZE)
    pool_addresses = []
    for i in range(n_batches):
        pool_addresses += query_contract.functions.getPairsByIndexRange(factory_address, i * BATCH_SIZE,
                                                                        (i + 1) * BATCH_SIZE).call()
    pool_addresses += query_contract.functions.getPairsByIndexRange(factory_address, n_batches * BATCH_SIZE,
                                                                    total_number_of_pools).call()
    return pool_addresses


# uniswap_weth_pool_addresses = get_pool_addresses(uniswap_factory_contract, address.uniswap_factory_address)
# suchiswap_weth_pool_addresses = get_pool_addresses(sushiswap_factory_contract, address.sushiswap_factory_address)


def get_weth_pool_addresses(pair_addresses):
    weth_pair_addresses = []
    for i in range(len(pair_addresses)):
        if pair_addresses[i][0] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' or pair_addresses[i][
            1] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            weth_pair_addresses.append(pair_addresses[i][2])
    return weth_pair_addresses


def get_reserves_from_addresses(lp_addresses):
    reserves_list = []
    n_batches = int(len(lp_addresses) / BATCH_SIZE)
    for i in range(n_batches):
        reserves_list += query_contract.functions.getReservesByPairs(
            lp_addresses[i * BATCH_SIZE: (i + 1) * BATCH_SIZE]).call()
    reserves_list += query_contract.functions.getReservesByPairs(
        lp_addresses[n_batches * BATCH_SIZE: len(reserves_list)]).call()
    return reserves_list


precompute_sushiswap = get_weth_pool_addresses(
    get_pool_addresses(address.sushiswap_factory_address))
precompute_uniswap = get_weth_pool_addresses(
    get_pool_addresses(address.uniswap_factory_address))
precompute_cro = get_weth_pool_addresses(
    get_pool_addresses(address.croswap_factory_address))
precompute_zeus = get_weth_pool_addresses(
    get_pool_addresses(address.zeus_factory_address))
precompute_lua = get_weth_pool_addresses(
    get_pool_addresses(address.lua_factory_address))

print(len(precompute_uniswap))
print(len(precompute_sushiswap))
print(len(precompute_cro))
print(len(precompute_zeus))
print(len(precompute_lua))
