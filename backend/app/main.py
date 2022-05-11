
#FastAPI
from fastapi import FastAPI, Depends
from cpu.models.config_model import ConfigIn
from cpu.models.process import ProcessIn
from multiprocessing import Process
from cpu.start import start
from typing import List

#From 3th
import uvicorn
import asyncio

app = FastAPI()


@app.get("/")
async def welcome():
    print("hello!")
    return "hi"

@app.post("/start")
def start_backend(config: ConfigIn, processes:List[ProcessIn]):
    p = Process(target=start, args=(config,processes))
    p.start()
    p.join()
    return {
        "config":config,
        "process":processes
    }



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)