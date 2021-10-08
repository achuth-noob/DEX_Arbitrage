import redis
from data.tokens import *
from multiprocessing import Process
import msgpack as mp
import subprocess
import pickle as pk
import pprint as pp
import time
import warnings
import json
warnings.filterwarnings("ignore")

redis_host = "localhost"
redis_port = 6379
staticdb_redis_obj = redis.StrictRedis(host = redis_host, 
        port=redis_port,db=0,decode_responses=True)
dataframedb_redis_obj = redis.StrictRedis(host = redis_host,
        port=redis_port,db=2,decode_responses=True)

l = {}
# To add new exchange info to dataframe generator DB.
def initial(msgpack_path):
    t = time.time()
    with open(msgpack_path,'r') as f:
        l.update(json.load(f))
        f.close()
    t1 = time.time()
    print(t1-t)

    for i in l:
        dataframedb_redis_obj.hmset(
            i,
            l[i]
        )
    print('Exchange added')

def setup_db():
    path = './data/sushiswap_pairs.json'
    initial(path)
    path = './data/uniswap_pairs.json'
    initial(path)
    with open('./data/allexchanges_pairs.json','w') as f:
        json.dump(l,f)
        f.close()

setup_db()

t = time.time()
with open('./data/allexchanges_pairs.json','r') as f:
    l = json.load(f)
    f.close()
# print(len(l))
t1 = time.time()
print(t1-t)