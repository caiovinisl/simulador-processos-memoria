from pydantic import BaseModel
from typing import Optional




class ProcessIn(BaseModel):
    name:str
    arrival_time:int
    execution_time:int
    deadline:int
    already_exec:Optional[int] = None

    def is_it_done(self):
        if self.execution_time <= self.already_exec:
            return True
        return False

class ProcessListIn(BaseModel):
    process_list: list[ProcessIn]