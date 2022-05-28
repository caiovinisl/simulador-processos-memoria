from typing import Dict, List
from collections import deque

class Memory:
    total_memory_pages: int
    current_space_occupied: int
    space_graph: Dict[int, bool]
    process_stack: deque
    type_name:str

    def __init__(self, type_name:str,total_memory_pages:int= 50,):
        self.total_memory_pages = total_memory_pages
        self.space_graph = self.space_initializer()
        self.current_space_occupied = 0
        self.process_stack = deque()
        self.type_name = type_name

    def space_initializer(self):
        space_graph = {}
        total_memory_pages = range(self.total_memory_pages)
        for i in total_memory_pages:
            space_graph[i] = False # lugar da memoria começa vazio
        return space_graph

    def does_it_fit(self, number_of_page_in: int):
        free_space = self.total_memory_pages - self.current_space_occupied 
        if free_space >= number_of_page_in:
            return True
        return False
    
    def empty_spaces(self):
        empty_list = []
        for i in range(self.total_memory_pages):
            if self.space_graph[i]:
                empty_list.append(i)
        return empty_list

    def add(self,used_index:List,pages:int)-> List[int]:
        counter=0
        for i in range(self.total_memory_pages):
            if counter == pages:#se forem alocadas o número de paginas, pare de alocar!
                break
            if not self.space_graph[i]:
                self.space_graph[i] = True
                self.current_space_occupied += 1
                used_index.append(i)
                counter+=1
        return used_index
      

    def remove(self,index_list:List[int]):
        if index_list is None:
            print("Process is not in memory")
        else:
            for index in index_list:
                self.space_graph[index] = False
                self.current_space_occupied -= 1
                print(f"Removed {index} from real memory")

    def add_stack(self,process):
        name = process.name
        if not name in self.process_stack:
            self.process_stack.appendleft(name)
        return True