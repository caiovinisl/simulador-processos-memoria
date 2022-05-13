import json
from typing import List

#DOCKER MOD
from cpu.models import config_model
from cpu.models import process
from cpu.configs.config import scalonator_translate,path,file_name
from cpu.driver import json_driver
from time import sleep

#DEBUG MODE
# from driver import json_driver
# from models import config_model
# from models import process
# from configs.config import scalonator_translate,path,file_name
#TODO: need cicle_data model
#TODO: Need memory logic!
#TODO: Need to comment code
#TODO: Overcharge

def start(config:config_model.ConfigIn, process_list:List[process.ProcessIn]):

    print("###########################")

    print("INSIDE NEW SUB-PROCESS")

    print("###########################")

    scalonator_engine =  scalonator_translate[config.scale_algorithm] 
    
    queue: list[process.ProcessIn] = scalonator_engine(process_list)
    print("Creates file")
    json_driver.create_file(path=path,file_name=file_name)
    cicle_id = 1

    print("enters main loop!")
    while queue:#Enquanto tiver algo na queue
        p = queue.pop() #Dentro do processador
        for quantum in range(config.quantum):
            p.already_exec +=1
            sleep(1)
            if p.is_it_done():
                print(f"process={p.name} its done!")
                break 
        '''
        FALTA A LOGICA DA MEMORIA
        FALTA A LOGICA DA MEMORIA
        FALTA A LOGICA DA MEMORIA
        FALTA A LOGICA DA MEMORIA
        FALTA A LOGICA DA MEMORIA
        FALTA A LOGICA DA MEMORIA
        '''
        if not p.is_it_done():
            queue.append(p) 
            queue = scalonator_engine(queue)

        cicle_data = create_cicle_data(0,0,0,p)

        json_driver.write(path,file_name,cicle_id,cicle_data=cicle_data)
        cicle_id+=1

            
def create_cicle_data(take, arguments, here, process:process.ProcessIn) -> dict:
    #do something with the arguments
    p_dict = process.dict()
    return {
                "what you need":{
                    process.name:p_dict
                }
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