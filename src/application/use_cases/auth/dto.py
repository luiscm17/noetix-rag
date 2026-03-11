from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterUserRequest:
    """Request to register a new user."""

    email: str
    username: str
    password: str


@dataclass
class LoginRequest:
    """Request to login a user."""

    email: str
    password: str
