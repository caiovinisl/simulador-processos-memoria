from distutils.command.build_scripts import first_line_re
import json
from typing import List, Tuple

from cpu.models import config_model
from cpu.models import process
from cpu.configs.config import scalonator_translate,path,file_name, turnover_file_name
from cpu.driver import json_driver
from time import sleep

#TODO: need cicle_data model
#TODO: Need memory logic!
#TODO: Need to comment code

def start(config:config_model.ConfigIn, process_list:List[process.ProcessIn]):

    print("###########################")

    print("INSIDE NEW SUB-PROCESS")

    print("###########################")
    print(f'qt process = {len(process_list)}')

    scalonator_engine =  scalonator_translate[config.scale_algorithm] 
    
    queue: list[process.ProcessIn] = scalonator_engine(process_list)
    json_driver.create_file(path=path,file_name=file_name)

    # main-loop variables
    cicle_id = 1
    threshold_quantum = config.quantum
    overhead = config.overhead
    math_turnover_util = []
    is_overhead = False
    cache_name = False
    is_process_done = False
    time_count = 0
    first = True
    print("enters main loop!")

    while queue:#Enquanto tiver algo na queue

        p = queue.pop() #Dentro do processador
        if p.name != cache_name: #Caso o process não esteja carregado na memoria
            # load_context MMU()
            
            is_overhead = True
            if not first:
                first = False
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
                math_turnover_util.append((p.name,time_count,p.arrival_time))
                print(f"process={p.name} its done!")
                break 
        
        #Fora do processador
        
        if not p.is_it_done():
            queue.append(p) 
            queue = scalonator_engine(queue)

        cicle_data = create_cicle_data(
            0,0,
            0,p,
            quantum,is_overhead,
            overhead,is_process_done,
            queue,time_count
        )

        json_driver.write(path,file_name,cicle_id,cicle_data=cicle_data)
        cicle_id+=1



    print("Calculating mean turnover")
    print(f'tuple = {math_turnover_util}')
    turnover_result = calculate_mean_turnover(math_turnover_util,len(process_list))
    json_driver.create_file(path=path,file_name=turnover_file_name)
    json_driver.write(path,turnover_file_name,0,turnover_result)
    json_driver.write(path,turnover_file_name,1,math_turnover_util)

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
    queue:List[process.ProcessIn],
    time_count:int
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
                "time":time_count
            }
    

if __name__ =="__main__":
    config=config_model.ConfigIn(
        scale_algorithm="FIFO",
        quantum=2,
        overchage=0
    )
    p1 = process.ProcessIn(
        name="1",
        arrival_time=0,
        execution_time=2,
        deadline=0
    )
    p2 = process.ProcessIn(
        name="2",
        arrival_time=0,
        execution_time=1,
        deadline=0
    ) 
    process_list = [p1,p2]
    start(config, process_list)
    print()