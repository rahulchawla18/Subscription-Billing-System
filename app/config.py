from pydantic_settings import BaseSettings

# Define a Settings class using Pydantic for managing environment variables
class Settings(BaseSettings):
    # Database connection URL (using SQLite as the default)
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Redis broker URL used by Celery for task queueing
    REDIS_BROKER_URL: str = "redis://localhost:6379/0"

# Create a settings instance to be imported and reused across the project
settings = Settings()
