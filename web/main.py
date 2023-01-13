import os
import sys
from injector import Injector
import uvicorn


path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path+'/src')
sys.path.append(path+'/src/infrastructure')

from src.infrastructure.app import create_app

app = create_app(Injector())

if __name__ == "__main__":
    uvicorn.run("main:app")
