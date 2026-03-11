from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict
import hashlib
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: Optional[int] = Field(default=None, description="User ID")
    username: str = Field(..., min_length=1, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email")
    password_hash: Optional[str] = Field(default=None, description="Password hash")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Is active")
    registration_date: Optional[datetime] = None

    def set_password(self, password: str) -> None:
        """Hash the password and store it."""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def is_admin(self) -> bool:
        """Check if the user has admin role."""
        return self.role == UserRole.ADMIN
