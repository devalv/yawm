# -*- coding: utf-8 -*-
"""Project exceptions."""
from typing import Any, Dict

from fastapi import HTTPException, status

_headers: Dict[str, Any] = {"WWW-Authenticate": "Bearer"}

CREDENTIALS_EX: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers=_headers,
)

INACTIVE_EX: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user.", headers=_headers
)


NOT_AN_OWNER: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not an owner.",
    headers=_headers,
)


USER_EXISTS_EX: HTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The user already exists.",
    headers=_headers,
)
