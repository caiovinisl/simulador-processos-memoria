from pydantic import BaseModel

class ProcessIn(BaseModel):
    name:str
    arrival_time:int
    execution_time:int
    deadline:int
    already_exec:int

    def is_it_done(self):
        if self.execution_time <= self.already_exec:
            return True
        return False

