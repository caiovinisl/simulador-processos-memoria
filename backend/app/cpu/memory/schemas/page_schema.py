from pydantic import BaseModel

class Page(BaseModel):
    size:int
    quantity:int
    uses:int
    process_name:str

    def __init__(self,quantity:int,process_name:str, uses:int = 0):
        self.quantity = quantity
        self.process_name = process_name
        self.uses = 1