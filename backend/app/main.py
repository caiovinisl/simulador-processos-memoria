
#FastAPI
from fastapi import FastAPI, Depends

#From 3th
import uvicorn
import asyncio



app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)