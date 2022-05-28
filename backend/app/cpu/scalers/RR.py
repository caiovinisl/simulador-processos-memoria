import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn
from collections import deque



def rr(process_list:list[ProcessIn],time_count:int=None)-> deque[ProcessIn]:
    d = deque()
    print('fazendo rr')
    d.append(process_list[len(process_list) - 1])
    for x in range(len(process_list)-2):
        d.append(process_list[x])
    return d

