from fastapi import FastAPI
from injector import Injector, SingletonScope
from fastapi_injector import attach_injector
from fastapi.middleware.cors import CORSMiddleware

from web.src.adapter.api.pps import pps_controller
from web.src.adapter.spi.repositories_factory import RepositoriesFactory

repositories_factory = RepositoriesFactory()

origins = [
    "http://localhost:8080",
]


def create_app(injector: Injector) -> FastAPI:
    app: FastAPI = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(pps_controller.router, prefix="/api/v1/pps", tags=["pps"])

    injector.binder.bind(RepositoriesFactory, to=repositories_factory, scope=SingletonScope)

    attach_injector(app, injector)

    return app
