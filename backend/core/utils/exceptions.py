# -*- coding: utf-8 -*-
"""Project exceptions."""

from fastapi import HTTPException, status


CREDENTIALS_EX = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
