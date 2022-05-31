import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn
from collections import deque



def edf(process_list:list[ProcessIn],time_count:int=None)-> deque[ProcessIn]:
    d = deque()
    print('fazendo edf')
    process_list.sort(key=lambda x: x.deadline, reverse=True)
    for x in process_list:
        d.append(x)
    return d

