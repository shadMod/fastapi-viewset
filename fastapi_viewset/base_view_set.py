from typing import Callable, Dict, List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .constants import (
    STATUS_BAD_REQUEST,
    STATUS_OK,
    STATUS_UNSUPPORTED_MEDIA_TYPE,
)


class BaseViewSet:
    prefix: str = ""
    tags: list[str] | None = None

    def __init__(self):
        if not self.prefix:
            raise ValueError("Ogni ViewSet deve avere un prefix.")
        self._router = APIRouter(prefix=self.prefix, tags=self.tags)
        self.actions: Dict[str, Dict] = {}
        self.register_default_routes()
        self.register_action_routes()

    async def list(self):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "list() not implemented.")

    async def retrieve(self):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "retrieve() not implemented.")

    async def create(self):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "create() not implemented.")

    async def update(self):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "update() not implemented.")

    async def partial_update(self):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "partial_update() not implemented.")

    async def delete(self):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "delete() not implemented.")

    def response_as_json(self, data, status: int | None = None):
        return JSONResponse({"success": True, "data": data}, status_code=status or STATUS_OK)

    def response_error(self, message, status: int | None = None):
        raise HTTPException(status or STATUS_BAD_REQUEST, message)

    def register_default_routes(self):
        self._router.add_api_route("/", self.list, methods=["GET"])
        self._router.add_api_route("/{item_id}", self.retrieve, methods=["GET"])
        self._router.add_api_route("/", self.create, methods=["POST"])
        self._router.add_api_route("/{item_id}", self.update, methods=["PUT"])
        self._router.add_api_route("/{item_id}", self.partial_update, methods=["PATCH"])
        self._router.add_api_route("/{item_id}", self.delete, methods=["DELETE"])

    @property
    def router(self) -> APIRouter:
        return self._router

    def register_action_routes(self):
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, "_is_action"):
                path = "/{item_id}" if method._detail else "/"
                self._router.add_api_route(
                    path + name + "/",
                    method,
                    methods=method._methods,
                    name=f"{self.prefix}-{name}",
                )

    @classmethod
    def action(cls, detail: bool, methods: List[str]):
        def decorator(func: Callable):
            func._is_action = True
            func._detail = detail
            func._methods = methods
            return func

        return decorator
