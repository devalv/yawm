# -*- coding: utf-8 -*-
"""Project exceptions."""

from fastapi import HTTPException, status

CREDENTIALS_EX = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

INACTIVE_EX = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Inactive user",
    headers={"WWW-Authenticate": "Bearer"},
)


OAUTH2_EX = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to get google OAuth data. Try to reload the page.",
    headers={"WWW-Authenticate": "Bearer"},
)


NOT_IMPLEMENTED_EX = HTTPException(
    status_code=status.HTTP_501_NOT_IMPLEMENTED, headers={"WWW-Authenticate": "Bearer"}
)
