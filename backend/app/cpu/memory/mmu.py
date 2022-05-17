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
            return True #Tudo certo! o processo já está carregado na memoria
        
        elif True and \
            ( real_virtual_map.get(process.name, None) ) and\
            ( real_virtual_map[process.name].get("virtual", None)
        ): #O processo não está na memo_real, mas está na memo_virtual
            if not self.memory_real.is_memory_full(process.pages): #caso a memoria real NÃO esteja cheia, alocar o processo
                real_used_index = self.add_to_memory(process.page,self.memory_real)
                self.real_virtual_map[process.name]["real"] = real_used_index #Fazer update da tabela hash
                self.real_virtual_map[process.name]["uses"] += 1 #Fazer update da tabela hash
                return True
            else: #Caso a memoria esteja cheia, vamos ao swap!
                real_virtual_map = self.swap(real_virtual_map)
                pass


        else:#O processo não tinha sido cadastrado antes!
            pass

        
        
       
    def add_to_memory(
        self,
        pages:int,
        memory: Union[MemoryReal,MemoryVirtual]
    )-> List[int]:
        used_index = []
        if not memory.is_memory_full(pages):
            for _ in range(pages): 
               used_index = memory.add(used_index)
            return used_index
        else:
            print("memory full!")


    def swap(self, process: ProcessIn):
        for k in self.real_virtual_map.keys():
            self.real_virtual_map[k]

        self.page_algorithm()

    def update_special_queue(self,page:Page):
        index = self.special_queue.index(page)
        self.special_queue.remove(page)

    def clean_done_process():
        pass

    def init_memory(self, process_list: List[ProcessIn]):
        pass

    def init_disk(self, process_list: List[ProcessIn]):
        pass

    
