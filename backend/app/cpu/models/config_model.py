from pydantic import BaseModel

class ConfigIn(BaseModel):
    scale_algorithm:str
    quantum:int
    overhead:int

