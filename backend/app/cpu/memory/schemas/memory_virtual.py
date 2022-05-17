from typing import Dict

class MemoryVirtual:
    total_memory_frames:int
    space_graph: Dict[str, bool]
    current_space_occupied: int


    def __ini__(self, total_memory_frames:int):
        self.total_memory_frame = total_memory_frames

    def space_initializer(self):
        space_graph = self.space_graph
        total_memory_pages = range(self.total_memory_pages)
        for i in total_memory_pages:
            space_graph[str(i)] = False # lugar da memoria começa vazio
        return space_graph

    def add(self,index:int):
        self.space_graph[str(index)] = True
        self.current_space_occupied += 1