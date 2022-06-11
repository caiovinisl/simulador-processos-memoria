import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn
from collections import deque



def sjf(process_list:list[ProcessIn],time_count:int=None)-> deque[ProcessIn]:
    d = deque()
    # print('fazendo sjf')
    process_list.sort(key=lambda x: x.execution_time - x.already_exec, reverse=True)
    for x in process_list:
        d.append(x)
    return d

