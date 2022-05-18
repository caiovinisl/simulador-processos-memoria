from distutils.command.build_scripts import first_line_re
import json
import re
from typing import List, Tuple
from collections import deque

from cpu.models import config_model
from cpu.models import process
from cpu.configs.config import scalonator_translate,path,file_name, turnover_file_name, swap_translate
from cpu.driver import json_driver
from cpu.memory.schemas.memory_real import MemoryReal
from cpu.memory.schemas.memory_virtual import MemoryVirtual
from cpu.memory.mmu import MMU

from time import sleep, time

#TODO: need cicle_data model
#TODO: Need memory logic!
#TODO: Need to comment code

def start(config:config_model.ConfigIn, process_list:List[process.ProcessIn]):

    print("###########################")

    print("INSIDE NEW SUB-PROCESS")

    print("###########################")

    scalonator_engine =  scalonator_translate[config.scale_algorithm] 
    page_algorithm = swap_translate[config.page_algorithm]
    
    json_driver.create_file(path=path,file_name=file_name)

    real_memory = MemoryReal(total_memory_pages=50)
    virtual_memory = MemoryVirtual(total_memory_frames=100)
    mmu = MMU(real_memory,virtual_memory,page_algorithm)
    # MMU.initialize(process_list)

    # main-loop variables
    cicle_id = 1
    threshold_quantum = config.quantum
    overhead = config.overhead
    done_process = []
    is_overhead = False
    cache_name = False
    is_process_done = False
    time_count = 0
    first = True
    queue: deque = deque()
    number_process = len(process_list)
    print("enters main loop!")

    while True:

        if len(done_process) >= number_process:
            mmu.garbage_collector(done_process)
            break

        to_enter = p_ready_to_enter(process_list,time_count)
        if to_enter:
            for ent in to_enter:
                queue.appendleft(ent)
            queue: deque[process.ProcessIn] = scalonator_engine(queue)

        if len(queue) != 0:
            p = queue.pop() #Dentro do processador
            started_time = time_count
        else:
            time_count+=1
            mmu.garbage_collector(done_process)
            continue

        if p.name != cache_name: #Caso o process não esteja carregado na cache
            result = MMU.load_context(p)
            
            is_overhead = True
            if not first:
                sleep(overhead)
                time_count+=1
            first = False
            
        else:
            is_overhead = False
        is_process_done = False
        cache_name = p.name
        

        for quantum in range(1, threshold_quantum+1):
            p.already_exec +=1
            time_count+= 1
            sleep(1)
            if p.is_it_done():
                is_process_done = True
                done_process.append((p.name,time_count,p.arrival_time))
                print(f"process={p.name} its done!")
                break 
        
        #Fora do processador
        
        if not p.is_it_done():
            queue.appendleft(p) 
            queue: deque = scalonator_engine(list(queue))

        cicle_data = create_cicle_data(
            0,0,
            0,p,
            quantum,is_overhead,
            overhead,is_process_done,
            queue,time_count,
            started_time
        )

        json_driver.write(path,file_name,cicle_id,cicle_data=cicle_data)
        cicle_id+=1



    print("Calculating mean turnover")
    print(f'tuple = {done_process}')
    turnover_result = calculate_mean_turnover(done_process,number_process)
    json_driver.create_file(path=path,file_name=turnover_file_name)
    json_driver.write(path,turnover_file_name,0,turnover_result)
    json_driver.write(path,turnover_file_name,1,done_process)

    print(f'turnover = {turnover_result}')
    print("Finish process")



def calculate_mean_turnover(
    math_util:List[Tuple[str,int,int]],
    number_process:int
) -> float:
    numerator = 0
    denominator = number_process
    for t in math_util:
        numerator += t[1] - t[2] #TurnarountTime - Arrival time
    turnover_result = numerator/denominator
    
    return turnover_result
    

def create_cicle_data(
    take,
    arguments,
    here,
    process:process.ProcessIn,
    quantum:int,
    is_overhead:bool,
    overhead:int,
    is_process_done:bool,
    queue:deque[process.ProcessIn],
    time_count:int,
    started_time:int
) -> dict:
    if is_overhead:
        overhead_response = overhead
    else:
        overhead_response = 0
    next_processess = [p.name for p in queue]
   

    #do something with the arguments
    p_dict = process.dict()
    return {
                "process":{
                    process.name:p_dict
                },
                "quantum":quantum,
                "overhead":overhead_response,
                "next_processess":next_processess,
                "done_in_this_cicle":is_process_done,
                "time":time_count,
                "started_time":started_time
            }
    

def p_ready_to_enter(
    process_list: List[process.ProcessIn],
    time_count:int
)-> List[process.ProcessIn]:
    result = []
    for index,p in enumerate(process_list):
        if time_count >= p.arrival_time:
            result.append(p)
            process_list.pop(index)
    return result
        

