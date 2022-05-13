import os, sys

# PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# result = os.path.split(PARENT)[0]
# sys.path.append(result)
from cpu.models.process import ProcessIn



def fifo(process_list:list[ProcessIn]):

    print('fazendo fifo')
    process_list2 = [x for x in process_list]
    return process_list2

