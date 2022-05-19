from typing import Dict, List

class MemoryVirtual:
    total_memory_frames: int
    current_memory_space: int
    space_graph: Dict[str, bool]

    def __init__(self, total_memory_frames:int= 100):
        self.total_memory_frames = total_memory_frames
        self.space_graph = self.space_initializer()
        self.current_space_occupied = 0

    def space_initializer(self):
        space_graph = {}
        total_memory_frames = range(self.total_memory_frames)
        for i in total_memory_frames:
            space_graph[i] = False # lugar da memoria começa vazio
        return space_graph

    def is_memory_full(self, number_of_page_in: int):
        if number_of_page_in > self.current_memory_space:
            return True
        return False
    
    def empty_spaces(self):
        empty_list = []
        for i in range(self.total_memory_frames):
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
        return used_index
      

    def remove(self,index_list:List[int]):
        for index in index_list:
            self.space_graph[index] = False
            self.current_space_occupied -= 1
            print(f"Removed {index} from real memory")

