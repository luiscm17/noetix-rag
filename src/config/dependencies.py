from functools import lru_cache
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.infrastructure.db.connection import get_db
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.services import BcryptHasher, JWTGenerator
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.domain.interfaces.token_generator import ITokenGenerator
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.entities.user import User
from src.application.use_cases.auth.register_user import RegisterUserUseCase
from src.application.use_cases.auth.login_user import LoginUserUseCase


security = HTTPBearer()


@lru_cache
def get_password_hasher() -> IPasswordHasher:
    """Get the password hashing service."""
    return BcryptHasher()


@lru_cache
def get_token_generator() -> ITokenGenerator:
    """Get the token generation service."""
    return JWTGenerator()


def get_user_repository(session: Session = Depends(get_db)) -> IUserRepository:
    """Get the user repository."""
    return UserRepository(session)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_gen: ITokenGenerator = Depends(get_token_generator),
    user_repo: IUserRepository = Depends(get_user_repository),
) -> User:
    """Get the current authenticated user from JWT token."""
    try:
        payload = token_gen.decode(credentials.credentials)
        email = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        user = user_repo.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_register_user_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    hasher: IPasswordHasher = Depends(get_password_hasher),
    token_gen: ITokenGenerator = Depends(get_token_generator),
) -> RegisterUserUseCase:
    """Get the user registration use case."""
    return RegisterUserUseCase(user_repo, hasher, token_gen)


def get_login_user_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
    hasher: IPasswordHasher = Depends(get_password_hasher),
    token_gen: ITokenGenerator = Depends(get_token_generator),
) -> LoginUserUseCase:
    """Get the user login use case."""
    return LoginUserUseCase(user_repo, hasher, token_gen)
