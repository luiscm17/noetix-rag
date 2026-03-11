from fastapi import APIRouter, Depends, HTTPException, status
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


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
):
    """Register a new user and return an authentication token."""
    result = use_case.execute(
        RegisterUserRequest(
            email=request.email, username=request.username, password=request.password
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
async def login(
    request: LoginSchema, use_case: LoginUserUseCase = Depends(get_login_user_use_case)
):
    """Login a user and return a JWT token."""
    result = use_case.execute(
        LoginRequest(email=request.email, password=request.password)
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
