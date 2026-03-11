from dataclasses  import dataclass
from datetime import datetime
from pydantic import EmailStr

@dataclass
class User:
    user_id: int
    user_name: str
    email: EmailStr
    password_hash: str
    role: str
    is_active: bool
    registration_date: datetime
