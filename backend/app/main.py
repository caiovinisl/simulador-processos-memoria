
#FastAPI
from multiprocessing import Process
from fastapi import FastAPI, Depends,HTTPException
from typing import List,Optional
from fastapi.middleware.cors import CORSMiddleware
from cpu.models.config_model import ConfigIn
from cpu.models.process import ProcessIn
from cpu.start import start
from cpu.driver import json_driver
from cpu.configs.config import path,file_name,turnover_file_name


#From 3th
import uvicorn
import asyncio

#TODO: Need response models!

app = FastAPI()

origins = [
    "http://localhost:8030",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

list_process: List[Process] = []

#Before it begins, it waits for the current processess to die
def join_process():
    print("fazendo join!")
    for p in list_process:
        # p.join()
        p.terminate()
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
    try:
        cicle_data = json_driver.read_cicle_id(
            path=path,
            file_name=file_name,
            cicle_id=cicle_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return cicle_data

@app.get("/cicle/get/")
def get_turnover():
    try:
    
        turnover_0 =  json_driver.read_cicle_id(
            path=path,
            file_name=turnover_file_name,
            cicle_id=0)
        turnover_1 =  json_driver.read_cicle_id(
            path=path,
            file_name=turnover_file_name,
            cicle_id=1)
    except Exception:
        raise HTTPException(status_code=404, detail="404")
    else:
        return {
            "turnover_mean": turnover_0,
            "p_tat": turnover_1
        }

@app.delete("/cicle/delete/all")
def delete_all_cicle():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8030, reload=True)
