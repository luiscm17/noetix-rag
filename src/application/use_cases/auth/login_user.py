from dataclasses import dataclass
from typing import Optional
from src.domain.entities.user import User
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.domain.interfaces.token_generator import ITokenGenerator
from .dto import LoginRequest


@dataclass
class LoginResponse:
    """Response to login a user."""

    user: Optional[User]
    access_token: str
    success: bool
    error: Optional[str] = None


class LoginUserUseCase:
    """Use case for user login."""

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        token_generator: ITokenGenerator,
    ):
        self._user_repo = user_repository
        self._hasher = password_hasher
        self._token_gen = token_generator

    def execute(self, request: LoginRequest) -> LoginResponse:
        """Execute the user login use case."""

        # Buscar usuario por email
        user = self._user_repo.get_by_email(request.email)
        if not user:
            return LoginResponse(
                user=None, access_token="", success=False, error="Invalid credentials"
            )

        # Verificar password
        if not self._hasher.verify(request.password, user.password_hash or ""):
            return LoginResponse(
                user=None, access_token="", success=False, error="Invalid credentials"
            )

        # Generar token
        token, _ = self._token_gen.generate(user)

        return LoginResponse(user=user, access_token=token, success=True)
