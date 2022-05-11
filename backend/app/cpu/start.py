import json
from typing import List
from models import config_model
from models import process
from scalers.FIFO import fifo
from time import sleep

scalonator_translate = {
    "FIFO": fifo
}

'''
Para rodar este código tanto pelo docker quanto pelo debugger, por favor esteja na pasta backend/
'''
def start():
    #Load configs and process
    process_dict, config_dict = load_configs_and_process()
    
    process_list = process_factory(process_dict)
    global config
    config = config_model.ConfigIn(
        scale_algorithm=config_dict["scale_algorithm"],
        quantum=config_dict["quantum"],
        overchage=config_dict["overchage"]
    )
    print(process_list)
    print(config)

    global scalonator_engine
    scalonator_engine =  scalonator_translate[config.scale_algorithm] 
    
    global queue
    queue = scalonator_engine(process_list)
    return queue



def get_info():
    while queue:#Enquanto tiver algo na queue
        
        p = queue.pop() #Dentro do processador
        for quantum in config.quantum:
            p.already_exec +=1
            sleep(1)
            if p.is_it_done():
                break 
        
        if p.is_it_done():
            logging.debug(INFO)
        else:
            queue.append(p) 
            queue = scalonator_engine(queue)
        


    



 
def load_configs_and_process():
    '''
    Uma rota deve enviar para esta função os jsons!
    E assim que o programa começa!
    '''
    with open("app/cpu/configs/process_file.json",'r') as file: #for docker
        process_dict = json.load(file)
    with open("app/cpu/configs/config_file.json",'r') as file: #on local debug
        config_dict = json.load(file)
    return (process_dict, config_dict)

def process_factory(process_dict:dict)-> List[process.ProcessIn]:
    process_list = []
    
    for k,v in process_dict.items():
        p=process.ProcessIn(
            name=v["name"],
            arrival_time=v["arrival_time"],
            execution_time=v["execution_time"],
            deadline=v["deadline"]
        )
        process_list.append(p)
    return process_list

if __name__ =="__main__":
    start()
    print()