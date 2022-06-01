from typing import Dict, List, Union, Callable, Tuple, Set
from collections import deque, Counter
from cpu.models.process import ProcessIn
from cpu.memory.schemas.memory_real import Memory
import json

class MMU:
    
    real_virtual_map: Dict[str,Dict[str,int]]
    memory_real: Memory
    memory_virtual: Memory
    swap_algorithm: Callable
    p_count: any
    p_order: deque

    def __init__(self,
        memory_real: Memory,
        memory_virtual:Memory,
        swap_algorithm:Callable
    )-> None:
        self.memory_real = memory_real
        self.memory_virtual = memory_virtual
        self.real_virtual_map = {}
        self.swap_algorithm = swap_algorithm
        self.p_count = None
        self.p_order = deque()
        self.counter = Counter()


    def initialize(self, queue:List[ProcessIn]):
        for p in queue:

            if self.memory_real.does_it_fit(p.pages):

                real_used_index = self.add_to_memory(p.pages,self.memory_real)
                virtual_used_index = self.add_to_memory(p.pages,self.memory_virtual)

                self.real_virtual_map[p.name] = {
                    "real":real_used_index,
                    "virtual":virtual_used_index,
                    "uses": 1
                }
            elif self.memory_virtual.does_it_fit(p.pages):
                virtual_used_index = self.add_to_memory(p.pages,self.memory_virtual)
                self.real_virtual_map[p.name] = {
                    "real":None,
                    "virtual":virtual_used_index,
                    "uses":1
                }
            else:
                print("Both memory is FULL! cut process")
                raise(KeyError)
        return True
                


    def load_context(self, process: ProcessIn)-> bool:
        real_virtual_map = self.real_virtual_map
        self.counter[process.name] +=1
        if not process.name in real_virtual_map:
            self.p_order.appendleft(process.name)
        
        
        if True and\
            ( real_virtual_map.get(process.name, None) ) and\
            ( real_virtual_map[process.name].get("real", None) 
        ):
            return False #Tudo certo! o processo já está carregado na memoria
            #Não precisa de OVERHEAD
        
        elif True and \
            ( real_virtual_map.get(process.name, None) ) and\
            ( real_virtual_map[process.name].get("virtual", None)
        ): #O processo não está na memo_real, mas está na memo_virtual
            if self.memory_real.does_it_fit(process.pages): #caso a memoria real NÃO esteja cheia, alocar o processo
                real_used_indexes = self.add_to_memory(process.pages,self.memory_real)

                self.real_virtual_map[process.name]["real"] = real_used_indexes #Fazer update da tabela hash
                return True
            else: #Caso a memoria esteja cheia, vamos ao swap!
                self.swap(process)
                

                return True


        else:#O processo não ta nem na memoria real nem na virtual
            if self.memory_real.does_it_fit(process.pages): #caso a memoria real NÃO esteja cheia, alocar o processo
                real_used_indexes = self.add_to_memory(process.pages,self.memory_real)
                virtual_used_indexes = self.add_to_memory(process.pages,self.memory_virtual)

                self.real_virtual_map[process.name] = {}
                self.real_virtual_map[process.name]["real"] = real_used_indexes
                self.real_virtual_map[process.name]["virtual"] = virtual_used_indexes
                return True

            else:#Caso a memoria real esteja cheia! Vamos de swap dnovo!
                virtual_used_indexes = self.add_to_memory(process.pages,self.memory_virtual)
                self.real_virtual_map[process.name] = {}
                self.real_virtual_map[process.name]["real"] = None
                self.real_virtual_map[process.name]["virtual"] = virtual_used_indexes
                self.swap(process)
                return True


        
        
       
    def add_to_memory(
        self,
        pages:int,
        memory: Union[Memory,Memory]
    )-> List[int]:
        used_index = []
        used_index = memory.add(used_index,pages)
        return used_index


    def swap(self, process: ProcessIn):
        #Enquanto não tiver espaço, fazer  o swap para ter espaço!
        
        removed_p_count = 1
        while not self.memory_real.does_it_fit(process.pages): 
            old_p_name= self.swap_algorithm(
                self.p_order, self.counter,removed_p_count)

            #Remove o index do processo antigo da memoria real
            list_index_to_remove = self.real_virtual_map[old_p_name]["real"]
            self.memory_real.remove(list_index_to_remove)
            self.real_virtual_map[old_p_name]["real"] = None
            self.counter[old_p_name] = 0

            removed_p_count+=1

        #cadastra o novo processo na memoria real
        real_used_indexes = self.add_to_memory(process.pages,self.memory_real)
        self.real_virtual_map[process.name]["real"] = real_used_indexes 
        self.counter[process.name] = 0 

        return True
         



    def garbage_collector_all(self,process_done:Tuple[str,int,int]):
        real_virtual_map = self.real_virtual_map
        for p_name,_,_ in process_done:
            free_real_indexes = real_virtual_map[p_name]["real"]
            free_virtual_indexes = real_virtual_map[p_name]["virtual"]

            self.memory_real.remove(free_real_indexes)
            self.memory_virtual.remove(free_virtual_indexes)


            real_virtual_map[p_name]["real"] = None
            real_virtual_map[p_name]["virtual"] = None
            real_virtual_map[p_name]["uses"] = 0
        self.real_virtual_map = real_virtual_map 
        print("Removed unused processes")

    def garbage_collector(self,process:ProcessIn):
            p_name = process.name
            real_virtual_map = self.real_virtual_map
            free_real_indexes = real_virtual_map[p_name]["real"]
            free_virtual_indexes = real_virtual_map[p_name]["virtual"]

            self.memory_real.remove(free_real_indexes)
            self.memory_virtual.remove(free_virtual_indexes)


            real_virtual_map[p_name]["real"] = None
            real_virtual_map[p_name]["virtual"] = None
            real_virtual_map[p_name]["uses"] = 0
            self.real_virtual_map = real_virtual_map 

            self.counter[p_name] = 0
            print(f"Removed processes = {p_name}")

    def show_real_virtual_map(self):
        copy = json.dumps(self.real_virtual_map)
        return copy

    def show_counter(self):
        copy = json.dumps(dict(self.counter))
        return copy
