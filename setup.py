from multiprocessing import Process
import subprocess
from setup_db import *
import time
import os

DATA_COLLECTOR_PATH = './event_listener.js'
DATA_PROCESS_PATH = './process_data.py'

def node_call(path,*args):
    print(f'Node script at {path} called......')
    p = subprocess.Popen(['node', path,*args], stdout=subprocess.PIPE)
    out = p.stdout.read()
    print(out)

def python_call(path,*args):
    print(f'Python script at {path} called......')
    p = subprocess.Popen(['python', path,*args], stdout=subprocess.PIPE)
    out = p.stdout.read()
    print(out)

if __name__=='__main__':
    p1 = Process(target=node_call,args=[DATA_COLLECTOR_PATH,])
    p2 = Process(target=python_call,args=[DATA_PROCESS_PATH,])
    p1.start()
    p2.start()
    p1.join()
    p2.join()