from web3 import Web3
import subprocess
import asyncio
import redis
import time
import json
import sys
import os

redis_host = "localhost"
redis_port = 6379
staticdb_redis_obj = redis.StrictRedis(host = redis_host, 
        port=redis_port,db=0,decode_responses=True)
dynamicdb_redis_obj = redis.StrictRedis(host = redis_host,
        port=redis_port,db=1,decode_responses=True)
dataframedb_redis_obj = redis.StrictRedis(host = redis_host,
        port=redis_port,db=2,decode_responses=True)
PROCESS_TIMEOUT = 300 # s

print('Script for Processing Data started..........')

class Process_Data(object):
    def __init__(self):
        self.last_block = 0
        self.curr_block = 0
        self.prev_t = time.time()
        self.curr_t = time.time()
        self.s_synced = False
        self.d_synced = False
        self.trig_response = False

        self.static_sync()

    def response(self):
        assert self.s_synced == True
        assert self.d_synced == True
        assert self.trig_response == True
        time.sleep(3)
        print('..................Response prepared')

    def monitor_data(self):
        pass

    def update_db(self):
        pass

    def decode_data(self,data_string):
        # Specific to topic
        tmp = data_string[2:]
        assert len(tmp)%64==0
        assert len(tmp[64:])==64
        return (int(tmp[:64],16),int(tmp[64:],16))

    def static_sync(self):
        p = subprocess.Popen(['node','./batch_request.js'], stdout=subprocess.PIPE)
        print(str(p.stdout.read()))
        self.curr_block=int(staticdb_redis_obj.get('blocknumber'))
        self.last_block=self.curr_block
        self.s_synced=True
        print('Static DB Synced....')

    def dynamic_sync(self):

        # from multiprocessing.connection import Listener

        # address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
        # listener = Listener(address, authkey='secret password')
        # conn = listener.accept()
        # print 'connection accepted from', listener.last_accepted
        # while True:
        #     msg = conn.recv()
        #     # do something with msg
        #     if msg == 'close':
        #         conn.close()
        #         break
        # listener.close()
        print('Data Synchronizing..................')
        with open('./data/cmn_unisushi_pairs.json','r') as f:
            unisushi = json.load(f)
            f.close()
        entries_left = int(dynamicdb_redis_obj.get('Cachedentries'))
        # ----------------Remove this once staticsynced---------------- 
        while entries_left!=0:
            entries_left-=1
            entry_id = dynamicdb_redis_obj.lpop('id')
            entry_reserves = self.decode_data(dynamicdb_redis_obj.lpop('data'))
            entry_blocknumber = dynamicdb_redis_obj.lpop('blocknumber')
            entry_addr = dynamicdb_redis_obj.lpop('address')
            entry_timestamp = dynamicdb_redis_obj.lpop('timestamp')
            try:
                dataframedb_redis_obj.lset(entry_addr,0,entry_reserves[0])
                dataframedb_redis_obj.lset(entry_addr,1,entry_reserves[1])
                unisushi[entry_addr]['reserve0'] = entry_reserves[0]
                unisushi[entry_addr]['reserve1'] = entry_reserves[1]
            except:
                # print('Missing addresses.......')
                staticdb_redis_obj.rpush('missing_addresses',entry_addr)
        self.curr_block = int(dynamicdb_redis_obj.get('latestblock'))
        self.last_block=self.curr_block
        self.d_synced=True
        self.trig_response=True

    def scan_data(self):
        # redis_obj.set('p_blocknumber',1200000)
        self.last_block = int(staticdb_redis_obj.get('blocknumber'))
        if self.last_block<self.curr_block:
            self.static_sync()
        while True:
            try:
                self.prev_t = int(dynamicdb_redis_obj.get('lastupdate'))
            except:
                print('Error while accessing timestamp in process_data class')
                self.prev_t = self.curr_t
                self.d_synced = False
            self.curr_t = int(time.time()*1000)
            self.curr_block = int(dynamicdb_redis_obj.get('latestblock'))
            if self.curr_t-self.prev_t>PROCESS_TIMEOUT and self.curr_block>self.last_block:
                self.dynamic_sync()
                self.response()
                print('waiting for new block..................')

p = Process_Data()
p.scan_data()
# p.static_sync()