
#FastAPI
from fastapi import FastAPI, Depends
from multiprocessing import Process
from typing import List,Optional


from cpu.models.config_model import ConfigIn
from cpu.models.process import ProcessIn
from cpu.start import start
from cpu.driver import json_driver
from cpu.configs.config import path,file_name


#From 3th
import uvicorn
import asyncio

#TODO: Need response models!
#TODO: Need delete cicle_log data!

app = FastAPI()

list_process = []

#Before it begins, it waits for the current processess to die
def join_process():
    print("fazendo join!")
    for p in list_process:
        p.join()
    return None



@app.get("/")
async def welcome():
    print("hello!")
    return "hi"

@app.post("/start")
def start_backend(
    config: ConfigIn,
    processes:List[ProcessIn],
    _ = Depends(join_process)
):
    p = Process(target=start, args=(config,processes))
    p.start()
    return {
        "msg":"sub-process created! Now go fetch the results",
        "config":config,
        "process":processes
    }



@app.get("/cicle/get/{cicle_id}")
def get_cicle(cicle_id:int)->None:
    cicle_data = json_driver.read_cicle_id(
        path=path,
        file_name=file_name,
        cicle_id=cicle_id)

    return cicle_data


@app.delete("/cicle/delete/all")
def delete_all_cicle():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)