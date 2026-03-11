from sqlalchemy.orm import Session
from src.domain.entities.user import User, UserRole
from src.domain.interfaces.user_repository import IUserRepository
from src.infrastructure.db.models import UserModel


class UserRepository(IUserRepository):
    """
    Repository to manage User entities in the database.
    Implements IUserRepository interface.
    """

    def __init__(self, db: Session):
        self._db = db

    def create(self, user: User) -> User:
        """Create a new user in the database."""
        role_value = user.role.value if hasattr(user.role, "value") else user.role

        model = UserModel(
            email=user.email,
            username=user.username,
            password_hash=user.password_hash,
            role=role_value,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def get_by_email(self, email: str) -> User | None:
        """Get a user by their email."""
        model = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def get_by_id(self, user_id: int) -> User | None:
        """Get a user by their ID."""
        model = self._db.query(UserModel).filter(UserModel.user_id == user_id).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: UserModel) -> User:
        """Convert a UserModel to a User entity."""
        return User(
            user_id=model.user_id,
            email=model.email,
            username=model.username,
            password_hash=model.password_hash,
            role=UserRole(model.role) if isinstance(model.role, str) else model.role,
            is_active=model.is_active,
            registration_date=model.registration_date,
        )
