from dataclasses import Field
from pydantic import BaseModel, Field
from typing import Optional

class ProcessIn(BaseModel):
    name:str
    arrival_time:int
    execution_time:int
    deadline:int
    pages:int = Field(lt=11)
    already_exec:Optional[int] = 0

    def is_it_done(self):
        if self.already_exec >= self.execution_time:
            return True
        return False

