
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password, verify_password
import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        hashed_password = hash_password(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User created: {user.email}")
        return db_user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
