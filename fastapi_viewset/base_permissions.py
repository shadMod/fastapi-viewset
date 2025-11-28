from typing import Any

from fastapi import Request


class BasePermissions:
    def has_permission(self, action: str, request: Request):
        return True

    def has_object_permission(self, action: str, obj: Any, request: Request):
        return True
