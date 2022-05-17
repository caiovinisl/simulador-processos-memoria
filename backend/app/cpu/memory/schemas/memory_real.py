from typing import Dict, List

class MemoryReal:
    total_memory_pages: int
    current_memory_space: int
    space_graph: Dict[str, bool]

    def __init__(self, total_memory_pages:int= 50):
        self.total_memory_pages = total_memory_pages
        self.space_graph = self.space_initializer()
        self.current_space_occupied = 0

    def space_initializer(self):
        space_graph = self.space_graph
        total_memory_pages = range(self.total_memory_pages)
        for i in total_memory_pages:
            space_graph[i] = False # lugar da memoria começa vazio
        return space_graph

    def is_memory_full(self, page_in: int):
        if page_in > self.current_memory_space:
            return True
        return False
    
    def empty_spaces(self):
        empty_list = []
        for i in range(self.total_memory_pages):
            if self.space_graph[i]:
                empty_list.append(i)
        return empty_list

    def add(self,used_index: List[any])-> List[int]:
        for i in range(self.total_memory_pages):
            if not self.space_graph[i]:
                self.space_graph[i] = True
                self.current_space_occupied += 1
                used_index.append(i)
        return used_index
      

    def remove(self,index:int):
        self.space_graph[str(index)] = False
        self.current_space_occupied -= 1


