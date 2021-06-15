import json
from keys import *
from tokens import *
from web3 import Web3
import address
import numpy as np

conn = Web3(Web3.HTTPProvider(provider))

BATCH_SIZE = 500

QUERY_ABI = json.load(open("assets/" + "IUniswapV2Query.json"))
query_contract = conn.eth.contract(address=Web3.toChecksumAddress(address.uniswap_query_address), abi=QUERY_ABI)

FACTORY_ABI = json.load(open("assets/" + "IUniswapV2Factory.json"))["abi"]
uniswap_factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(address.uniswap_factory_address),
                                             abi=FACTORY_ABI)
sushiswap_factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(address.sushiswap_factory_address),
                                               abi=FACTORY_ABI)

TOKEN_ABI = json.load(open("assets/" + "IUniswapV2ERC20.json"))["abi"]


def get_pool_addresses(factory_address):
    factory_contract = conn.eth.contract(address=Web3.toChecksumAddress(factory_address), abi=FACTORY_ABI)
    total_number_of_pools = factory_contract.functions.allPairsLength().call()
    n_batches = int(total_number_of_pools / BATCH_SIZE)
    pool_addresses = np.empty([total_number_of_pools, 3], dtype='<U42')
    for i in range(n_batches):
        pool_addresses[i * BATCH_SIZE:(i + 1) * BATCH_SIZE] = query_contract.functions.getPairsByIndexRange(
            factory_address, i * BATCH_SIZE,
            (i + 1) * BATCH_SIZE).call()
    pool_addresses[n_batches * BATCH_SIZE:] = query_contract.functions.getPairsByIndexRange(factory_address,
                                                                                            n_batches * BATCH_SIZE,
                                                                                            total_number_of_pools).call()
    return pool_addresses


uniswap_pool_address = get_pool_addresses(address.uniswap_factory_address)
np.save('uniswap_pool_addresses.npy', uniswap_pool_address)

sushiswap_pool_address = get_pool_addresses(address.sushiswap_factory_address)
np.save('sushiswap_pool_addresses.npy', sushiswap_pool_address)


def get_weth_pool_addresses(pair_addresses):
    weth_pair_addresses = []
    for i in range(len(pair_addresses)):
        if pair_addresses[i][0] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' or pair_addresses[i][
            1] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
            weth_pair_addresses.append(pair_addresses[i])
    return np.array(weth_pair_addresses)


uniswap_weth_pool_address = get_weth_pool_addresses(uniswap_pool_address)
np.save('uniswap_weth_pool_address.npy', uniswap_weth_pool_address)
sushiswap_weth_pool_address = get_weth_pool_addresses(sushiswap_pool_address)
np.save('sushiswap_weth_pool_address.npy', sushiswap_weth_pool_address)


def get_reserves_from_addresses(pool_addresses):
    reserves_list = np.empty([len(pool_addresses), 3], dtype='<U42')
    n_batches = int(len(pool_addresses) / BATCH_SIZE)
    for i in range(n_batches):
        reserves_list[i * BATCH_SIZE: (i + 1) * BATCH_SIZE] = np.array(query_contract.functions.getReservesByPairs(list(pool_addresses[i * BATCH_SIZE: (i + 1) * BATCH_SIZE, 2])).call())
    reserves_list[n_batches * BATCH_SIZE:, :] = query_contract.functions.getReservesByPairs(
        list(pool_addresses[n_batches * BATCH_SIZE:, 2])).call()
    return reserves_list



uniswap_reserves = get_reserves_from_addresses(uniswap_weth_pool_address)
np.save('uniswap_reserves.npy', uniswap_reserves)
sushiswap_reserves = get_reserves_from_addresses(sushiswap_weth_pool_address)
np.save('sushiswap_reserves.npy', sushiswap_reserves)

pool_order_uni = []
pool_order_sushi = []
intersection = []
for pool1 in uniswap_weth_pool_address:
    for pool2 in sushiswap_weth_pool_address:
        if np.array_equal(pool1[:2], pool2[:2]):
            pool_order_uni.append(pool1[2])
            pool_order_sushi.append(pool2[2])
            intersection.append(pool2)

len(intersection)
intersection = np.array(intersection)

pool_order = pool_order_uni + pool_order_sushi


def get_reserves_from_addresses_temp(pool_addresses):
    reserves_list = np.empty([len(pool_addresses), 3], dtype='<U42')
    n_batches = int(len(pool_addresses) / BATCH_SIZE)
    for i in range(n_batches):
        reserves_list[i * BATCH_SIZE: (i + 1) * BATCH_SIZE] = np.array(query_contract.functions.getReservesByPairs(list(pool_addresses[i * BATCH_SIZE: (i + 1) * BATCH_SIZE])).call())
    reserves_list[n_batches * BATCH_SIZE:, :] = query_contract.functions.getReservesByPairs(
        list(pool_addresses[n_batches * BATCH_SIZE:])).call()
    return reserves_list


temp = np.argwhere(intersection == Web3.toChecksumAddress(tokens["WETH"]['address']))
temp1 = np.argwhere(temp[:, 1] == 1)
temp2 = np.append(temp1, temp1 + len(temp1))

reserves = get_reserves_from_addresses_temp(pool_order)[:, :2]
reserves[temp2] = reserves[temp2][::-1]

reserves_combined = np.hstack((reserves[:len(reserves)//2], reserves[len(reserves)//2:]))
reserves_combined = reserves_combined.astype(np.float32, copy=False)

f_1 = f_2 = 0.997

ra_1 = reserves_combined[:, 0]/10**18
rb_1 = reserves_combined[:, 1]/10**18
ra_2 = reserves_combined[:, 2]/10**18
rb_2 = reserves_combined[:, 3]/10**18

a = ra_2 * rb_1 * f_1 * f_2
b = rb_1 * f_1 * f_2 + f_1 * rb_2
c = ra_1 * rb_2

x = (np.sqrt(a * c) - c) / b
y = (np.sqrt(a) - np.sqrt(c))**2/b

x_possible = x[a > c]
y_possible = y[a > c]
print(np.max(x_possible))
print(np.max(y_possible))
