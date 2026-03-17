from dataclasses import dataclass
from typing import Optional
from src.domain.entities.user import User, UserRole
from src.domain.interfaces.user_repository import IUserRepository
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.domain.interfaces.token_generator import ITokenGenerator
from .dto import RegisterUserRequest


@dataclass
class RegisterUserResponse:
    """Response to register a new user."""

    user: Optional[User]
    access_token: str
    success: bool
    error: Optional[str] = None


class RegisterUserUseCase:
    """Use case for registering a new user."""

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        token_generator: ITokenGenerator,
    ):
        self._user_repo = user_repository
        self._hasher = password_hasher
        self._token_gen = token_generator

    def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        """Execute the user registration use case."""

        # Validar que el email no exista
        existing = self._user_repo.get_by_email(request.email)
        if existing:
            return RegisterUserResponse(
                user=None,
                access_token="",
                success=False,
                error="Email already registered",
            )

        # Create new user
        user = User(
            username=request.username,
            email=request.email,
            password_hash=self._hasher.hash(request.password),
            role=UserRole.USER,
        )

        # Save user to repository
        saved_user = self._user_repo.create(user)

        # Generate token
        token, _ = self._token_gen.generate(saved_user)

        return RegisterUserResponse(user=saved_user, access_token=token, success=True)
