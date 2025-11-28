from typing import Any

from fastapi import HTTPException, Request

from .constants import STATUS_NOT_FOUND, STATUS_UNSUPPORTED_MEDIA_TYPE


class BaseCrudView:
    queryset: list[Any] | None = None

    def before_action(self, action: str, request: Request, *args, **kwargs):
        pass

    async def async_before_action(self, action: str, request: Request, *args, **kwargs):
        pass

    def after_action(self, action: str, result: Any):
        return result

    async def async_after_action(self, action: str, result: Any):
        return result

    def get_queryset(self):
        return self.queryset or []

    async def aget_queryset(self):
        return self.queryset or []

    def filter_queryset(self, request: Request):
        return self.queryset

    async def afilter_queryset(self, request: Request):
        return self.queryset

    def order_queryset(self, request: Request):
        return self.queryset

    def paginate_queryset(self, request: Request):
        return self.queryset

    def get_object(self, item_id):
        qs = self.get_queryset()
        for obj in qs:
            if str(obj.get("id")) == str(item_id):
                return obj
        return None

    async def aget_object(self, item_id):
        qs = self.get_queryset()
        for obj in qs:
            if str(obj.get("id")) == str(item_id):
                return obj
        return None

    async def list(self, request: Request):
        return await self.aget_queryset()

    async def retrieve(self, item_id: Any, request: Request):
        obj = await self.aget_object(item_id)
        if not obj:
            raise HTTPException(STATUS_NOT_FOUND, "Oggetto non trovato")
        return obj

    async def create(self, data: Any, request: Request):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "create() non implementato")

    async def update(self, item_id: Any, data: Any, request: Request):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "update() non implementato")

    async def partial_update(self, item_id: Any, data: Any, request: Request):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "partial_update() non implementato")

    async def delete(self, item_id: Any, request: Request):
        raise HTTPException(STATUS_UNSUPPORTED_MEDIA_TYPE, "delete() non implementato")
