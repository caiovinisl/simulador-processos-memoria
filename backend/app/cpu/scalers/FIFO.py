import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn
from collections import deque



def fifo(process_list:list[ProcessIn])-> deque[ProcessIn]:
    d = deque()
    print('fazendo fifo')
    for x in process_list:
        d.appendleft(x)
    return d

