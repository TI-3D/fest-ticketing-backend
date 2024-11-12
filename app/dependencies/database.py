from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine with the provided database URI
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,  # e.g., 'postgresql+asyncpg://user:password@localhost/dbname'
    echo=True,
    future=True,  # Required for compatibility with SQLAlchemy 2.x
    pool_pre_ping=True,  # Ensures connections are alive before use
)

# Session factory
# Using sessionmaker to bind to the engine and create AsyncSession objects
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Keeps objects after commit (avoid session refresh issues)
)

# Dependency for creating async database session
async def get_db() -> AsyncSession:
    # Create a new session, yield it to the route or function, and close it when done
    async with AsyncSessionLocal() as session:
        yield session
