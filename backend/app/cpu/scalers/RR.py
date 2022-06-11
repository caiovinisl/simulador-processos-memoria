import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn
from collections import deque
from typing import Union, List



def rr_v1(process_list:list[ProcessIn],time_count:int=None)-> deque[ProcessIn]:
    d = deque()
    # print('fazendo rr')
    d.append(process_list[len(process_list) - 1])
    for x in range(len(process_list)-2):
        d.append(process_list[x])
    return d


def rr_v2(
    process_list:list[ProcessIn],
    time_count:int=None,
    right:bool=False
)-> deque[ProcessIn]:
    d = deque()
    print('fazendo rr')

    for x in process_list:
        d.append(x)


    if right:
        d.rotate()#rodar para a direita!

    return d

def rr_v3(
    process_list:list[ProcessIn],
    add_p:Union[list[ProcessIn],ProcessIn],
    time_count:int=None,
)-> deque[ProcessIn]:
    d = deque()
    print('fazendo rr')

    for x in process_list:
        d.append(x)

    if type(add_p) is list:
        for p in add_p:
            d.append(p)
    elif type(add_p) is ProcessIn:
        d.appendleft(add_p)
   
    return d

def rr(process_list:list[ProcessIn],time_count:int=None):
    d = deque()
    lesser = 9999
    for x in process_list:
        if x.already_exec < lesser:
            lesser = x.already_exec
    normalized = all([p.already_exec==lesser if p.already_exec!=0 else False for p in process_list])
    if not normalized:        
        process_list.sort(key=lambda x: x.already_exec - lesser, reverse=True)
    else:
        process_list=reversed(process_list)


    for x in process_list:
        d.append(x)
    return d