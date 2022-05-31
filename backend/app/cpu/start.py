from distutils.command.build_scripts import first_line_re
import json
import re
from typing import Callable, List, Tuple, Dict
from collections import deque

from cpu.models import config_model
from cpu.models import process
from cpu.configs.config import scalonator_translate,path,file_name, turnover_file_name, swap_translate
from cpu.driver import json_driver
from cpu.memory.schemas.memory_real import Memory
from cpu.memory.mmu import MMU

from time import sleep, time

#TODO: need cicle_data model
#TODO: Need memory logic!
#TODO: Need to comment code

def start(config:config_model.ConfigIn, process_list:List[process.ProcessIn]):

    print("###########################")

    print("INSIDE NEW SUB-PROCESS")

    print("###########################")

    scalonator_engine: Callable =  scalonator_translate[config.scale_algorithm] 
    swap_algorithm: Callable = swap_translate[config.page_algorithm]
    
    json_driver.create_file(path=path,file_name=file_name)

    real_memory = Memory("real",total_memory_pages=10)
    virtual_memory = Memory("virtual",total_memory_pages=100)
    mmu = MMU(real_memory,virtual_memory,swap_algorithm)
    # mmu.initialize(process_list)
    # main-loop variables
    cicle_id = 1
    threshold_quantum = config.quantum
    overhead = config.overhead
    done_process = []
    is_overhead = False
    is_process_done = False
    time_count = 0
    first = True
    queue: deque = deque()
    number_process = len(process_list)
    real_virtual_map = None
    print("enters main loop!")

    while True:

        if len(done_process) >= number_process:
            # mmu.garbage_collector(done_process)
            break

        to_enter = p_ready_to_enter(process_list,time_count)
        # print("processos prontos a entrar em " + str(time_count) + ":  " + str(to_enter))
        if to_enter:
            for ent in to_enter:
                queue.appendleft(ent)
            # print("processos no escalonador em " + str(time_count) + ":  " + str(queue))
            queue: deque[process.ProcessIn] = scalonator_engine(list(queue),time_count=time_count)

        if len(queue) != 0:
            p = queue.pop() #Dentro do processador
            started_time = time_count
            is_process_done = False

        else:
            time_count+=1
            # mmu.garbage_collector(done_process)
            continue

        #Retorna True caso precise trocar de contexto!
        if mmu.load_context(p):
            if not first:
                is_overhead = True
                sleep(overhead)
                time_count+=overhead
            first = False
        else: #Retorna False caso o contexto já estava carregado
            is_overhead = False
        is_process_done = False
        
        # if p.name != cache_name: #Caso o process não esteja carregado na cache
        #     result = mmu.load_context(p)
            
        #     is_overhead = True
        #     if not first:
        #         sleep(overhead)
        #         time_count+=overhead
        #     first = False
            
        # else:
        #     is_overhead = False
        # is_process_done = False
        # cache_name = p.name
        

        for quantum in range(1, threshold_quantum+1):
            p.already_exec +=1
            p.deadline -= 1
            time_count+= 1
            sleep(0)
            if p.is_it_done():
                is_process_done = True
                done_process.append((p.name,time_count,p.arrival_time))
                real_virtual_map = mmu.show_real_virtual_map()

                mmu.garbage_collector(p)

                print(f"process={p.name} its done!")
                break 
        
        #Fora do processador
        
        if not p.is_it_done():
            real_virtual_map = mmu.show_real_virtual_map()
            queue.append(p) 
            queue: deque = scalonator_engine(list(queue),time_count=time_count)

        cicle_data = create_cicle_data(
            0,0,
            0,p,
            quantum,is_overhead,
            overhead,is_process_done,
            queue,time_count,
            started_time,
            real_virtual_map
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
    started_time:int,
    real_virtual_map: str
) -> dict:
    if is_overhead:
        overhead_response = overhead
    else:
        overhead_response = 0
    next_processess = [p.name for p in queue]
   

    #do something with the arguments
    p_dict = process.dict()
    memory_map =json.loads(real_virtual_map)
    return {
                "process":p_dict,
                "quantum":quantum,
                "overhead":overhead_response,
                "next_processess":next_processess,
                "done_in_this_cicle":is_process_done,
                "time":time_count,
                "started_time":started_time,
                "real_virtual_map": memory_map
            }
    

def p_ready_to_enter(
    process_list: List[process.ProcessIn],
    time_count:int
)-> List[process.ProcessIn]:
    result = []

    process_copy = process_list.copy()

    for p in process_copy:
        if time_count >= p.arrival_time:
            result.append(p)
            process_list.remove(p)

            # process_list.pop(index)
    return result
        

