from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.application.use_cases.auth.register_user import (
    RegisterUserUseCase,
    RegisterUserRequest,
)
from src.application.use_cases.auth.login_user import LoginUserUseCase, LoginRequest
from src.config.dependencies import get_register_user_use_case, get_login_user_use_case
from src.api.schemas.auth import (
    RegisterRequest,
    LoginRequest as LoginSchema,
    AuthResponse,
    UserResponse,
)
from src.api.dependencies import get_current_user
from src.domain.entities.user import User
from src.infrastructure.services.jwt_generator import JWTGenerator
from src.infrastructure.services.token_revocation import (
    get_token_revocation_service,
    TokenRevocationService,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    register_request: RegisterRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
):
    """Register a new user and return an authentication token."""
    result = use_case.execute(
        RegisterUserRequest(
            email=register_request.email,
            username=register_request.username,
            password=register_request.password,
        )
    )

    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.error
        )

    if result.user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed",
        )

    user = result.user
    return AuthResponse(
        access_token=result.access_token,
        user=UserResponse(
            user_id=user.user_id if user.user_id is not None else 0,
            email=user.email,
            username=user.username,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
        ),
    )


@router.post("/login", response_model=AuthResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_request: LoginSchema,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case),
):
    """Login a user and return a JWT token."""
    result = use_case.execute(
        LoginRequest(email=login_request.email, password=login_request.password)
    )

    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=result.error
        )

    if result.user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        )

    user = result.user
    return AuthResponse(
        access_token=result.access_token,
        user=UserResponse(
            user_id=user.user_id if user.user_id is not None else 0,
            email=user.email,
            username=user.username,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
        ),
    )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    revocation_service: TokenRevocationService = Depends(get_token_revocation_service),
):
    """Logout user by revoking their JWT token."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        jwt_generator = JWTGenerator()
        jti = jwt_generator.get_jti(token)
        ttl = jwt_generator.get_remaining_ttl(token)

        if jti and ttl > 0:
            revocation_service.revoke(jti, ttl)

    return {"message": "Successfully logged out"}
