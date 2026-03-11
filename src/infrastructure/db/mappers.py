from src.domain.entities import (
    User,
    UserRole,
    Document,
    DocumentStatus,
    Conversation,
    Message,
)
from src.infrastructure.db.models import (
    UserModel,
    DocumentModel,
    ConversationModel,
    MessageModel,
)


def map_user_to_model(user: User) -> UserModel:
    """Map a User domain entity to a UserModel database model."""
    role_value = user.role.value if hasattr(user.role, "value") else user.role
    return UserModel(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        role=role_value,
        is_active=user.is_active,
        registration_date=user.registration_date,
    )


def map_model_to_user(user_model: UserModel) -> User:
    """Map a UserModel database model to a User domain entity."""
    return User(
        user_id=user_model.user_id,
        username=user_model.username,
        email=user_model.email,
        password_hash=user_model.password_hash,
        role=UserRole(user_model.role)
        if isinstance(user_model.role, str)
        else user_model.role,
        is_active=user_model.is_active,
        registration_date=user_model.registration_date,
    )


def map_document_to_model(document: Document) -> DocumentModel:
    """Map a Document domain entity to a DocumentModel database model."""
    status_value = (
        document.status.value if hasattr(document.status, "value") else document.status
    )
    return DocumentModel(
        document_id=document.document_id,
        title=document.title,
        file_path=document.file_path,
        page_count=document.page_count,
        processed=status_value == "processed"
        if isinstance(status_value, str)
        else False,
        created_at=document.created_at,
        updated_at=document.updated_at,
        tags=document.tags,
    )


def map_model_to_document(document_model: DocumentModel) -> Document:
    """Map a DocumentModel database model to a Document domain entity."""
    status = (
        DocumentStatus.PROCESSED if document_model.processed else DocumentStatus.PENDING
    )
    return Document(
        document_id=document_model.document_id,
        title=document_model.title,
        file_path=document_model.file_path,
        page_count=document_model.page_count,
        created_at=document_model.created_at,
        updated_at=document_model.updated_at,
        tags=document_model.tags,
        status=status,
    )


def map_conversation_to_model(conversation: Conversation) -> ConversationModel:
    """Map a Conversation domain entity to a ConversationModel database model."""
    return ConversationModel(
        conversation_id=conversation.conversation_id,
        user_id=conversation.user_id,
        document_id=conversation.document_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


def map_model_to_conversation(conversation_model: ConversationModel) -> Conversation:
    """Map a ConversationModel database model to a Conversation domain entity."""
    return Conversation(
        conversation_id=conversation_model.conversation_id,
        user_id=conversation_model.user_id,
        document_id=conversation_model.document_id,
        title=conversation_model.title,
        created_at=conversation_model.created_at,
        updated_at=conversation_model.updated_at,
    )


def map_message_to_model(message: Message) -> MessageModel:
    """Map a Message domain entity to a MessageModel database model."""
    return MessageModel(
        message_id=message.message_id,
        conversation_id=message.conversation_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at,
    )


def map_model_to_message(message_model: MessageModel) -> Message:
    """Map a MessageModel database model to a Message domain entity."""
    return Message(
        message_id=message_model.message_id,
        conversation_id=message_model.conversation_id,
        role=message_model.role,
        content=message_model.content,
        created_at=message_model.created_at,
    )
