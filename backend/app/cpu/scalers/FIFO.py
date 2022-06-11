import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn
from collections import deque
from typing import Union, List



def fifo(process_list:list[ProcessIn],time_count:int=None)-> deque[ProcessIn]:
    d = deque()
    # print('fazendo fifo')
    for x in process_list:
        d.append(x)
    return d

def fifo_dont_use(
    process_list:list[ProcessIn],
    add_p:Union[list[ProcessIn],ProcessIn],
    time_count:int=None,
)-> deque[ProcessIn]:
    d = deque()
    print('fazendo fifo')
    for x in process_list:
        d.append(x)

    if type(add_p) is list:
        for p in add_p:
            d.appendleft(p)
    elif type(add_p) is ProcessIn:
        d.append(add_p)

    return d