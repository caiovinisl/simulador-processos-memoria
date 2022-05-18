from typing import Dict, List, Union, Callable
from collections import deque
from cpu.models.process import ProcessIn
from cpu.memory.schemas.memory_real import MemoryReal
from cpu.memory.schemas.memory_virtual import MemoryVirtual
from cpu.memory.schemas.page_schema import Page


class MMU():
    
    real_virtual_map: Dict[str,Dict[str,int]]
    memory_real: MemoryReal
    memory_virtual: MemoryVirtual
    special_queue: deque[Page]
    page_algorithm: Callable
    

    def __init__(self,memory_real: MemoryReal, memory_virtual:MemoryVirtual):
        self.memory_real = memory_real
        self.memory_virtual = memory_virtual
        self.real_virtual_map = {}
        self.special_queue: deque[Page] = deque()

    def initialize(self, queue:List[ProcessIn]):
        for p in queue:
            page = Page(quantity=p.pages,process_name=p.name)
            self.special_queue.appendleft(page)

            if not self.memory_real.is_memory_full(p.pages):

                real_used_index = self.add_to_memory(p.pages,self.memory_real)
                virtual_used_index = self.add_to_memory(p.pages,self.memory_virtual)

                self.real_virtual_map[p.name] = {
                    "real":real_used_index,
                    "virtual":virtual_used_index,
                    "uses": 1
                }
            elif not self.memory_virtual.is_memory_full(p.pages):
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
                


    def load_context(self, process: ProcessIn):
        real_virtual_map = self.real_virtual_map
        if True and\
            ( real_virtual_map.get(process.name, None) ) and\
            ( real_virtual_map[process.name].get("real", None) 
        ):
            self.real_virtual_map[process.name]["uses"] += 1 #Fazer update da tabela hash
            return True #Tudo certo! o processo já está carregado na memoria
        
        elif True and \
            ( real_virtual_map.get(process.name, None) ) and\
            ( real_virtual_map[process.name].get("virtual", None)
        ): #O processo não está na memo_real, mas está na memo_virtual
            if not self.memory_real.is_memory_full(process.pages): #caso a memoria real NÃO esteja cheia, alocar o processo
                real_used_indexes = self.add_to_memory(process.page,self.memory_real)
                self.real_virtual_map[process.name]["real"] = real_used_indexes #Fazer update da tabela hash
                self.real_virtual_map[process.name]["uses"] += 1 #Fazer update da tabela hash
                return True
            else: #Caso a memoria esteja cheia, vamos ao swap!
                self.swap(process)
                

                return True


        else:#O processo não ta nem na memoria real nem na virtual
            if not self.memory_real.is_memory_full(process.pages): #caso a memoria real NÃO esteja cheia, alocar o processo
                self.memory_real.add_stack(process)
                real_used_indexes = self.add_to_memory(process.page,self.memory_real)
                virtual_used_indexes = self.add_to_memory(process.page,self.memory_virtual)

                self.real_virtual_map[process.name]["real"] = real_used_indexes
                self.real_virtual_map[process.name]["virtual"] = virtual_used_indexes
            else:#Caso a memoria real esteja cheia! Vamos de swap dnovo!
                self.swap(process)



        
        
       
    def add_to_memory(
        self,
        pages:int,
        memory: Union[MemoryReal,MemoryVirtual]
    )-> List[int]:
        used_index = []
        for _ in range(pages): 
            used_index = memory.add(used_index)
        return used_index


    def swap(self, process: ProcessIn):

        new_p_real_index, old_p_name= self.page_algorithm(
            self.memory_real,
            process,
            self.real_virtual_map)

        #Remove o index do processo antigo da memoria real
        list_index_to_remove = self.real_virtual_map[old_p_name]["real"]
        self.memory_real.remove(list_index_to_remove)

        #Atualiza a remoção na hash table
        self.real_virtual_map[old_p_name]["real"] = None
        self.real_virtual_map[old_p_name]["uses"] = 0 #Fazer update da tabela hash

        #
        self.real_virtual_map[process.name]["real"] = new_p_real_index #Fazer update da tabela hash
        self.real_virtual_map[process.name]["uses"] += 1 #Fazer update da tabela hash

        return True
         

    def update_special_queue(self,page:Page):
        index = self.special_queue.index(page)
        self.special_queue.remove(page)

    def garbage_collector(self,process_done:List[ProcessIn]):
        real_virtual_map = self.real_virtual_map
        for p in process_done:
            free_real_index = real_virtual_map[p.name]["real"]
            free_virtual_index = real_virtual_map[p.name]["virtual"]

            self.memory_real.remove(free_real_index)
            self.memory_virtual.remove(free_virtual_index)


            real_virtual_map[p.name]["real"] = None
            real_virtual_map[p.name]["virtual"] = None
            real_virtual_map[p.name]["uses"] = None
        self.real_virtual_map = real_virtual_map 
        print("Removed unused processes")


    def init_memories(self):
        pass

    
