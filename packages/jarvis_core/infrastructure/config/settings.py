"""Configuration settings for the JARVIS application."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings using pydantic-settings.
    
    Loads configuration from environment variables with .env file support.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API server host")
    api_port: int = Field(default=8000, description="API server port")
    api_debug: bool = Field(default=False, description="Enable debug mode")
    api_reload: bool = Field(default=False, description="Enable auto-reload")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.7, description="Temperature for generation")
    openai_max_tokens: int = Field(default=2000, description="Max tokens per request")
    openai_timeout: int = Field(default=60, description="API request timeout in seconds")
    
    # Memory Configuration
    memory_base_path: str = Field(default="memory", description="Base path for memory storage")
    memory_type: str = Field(default="file", description="Memory storage type")
    memory_auto_backup: bool = Field(default=True, description="Enable automatic backups")
    memory_backup_interval: int = Field(default=86400, description="Backup interval in seconds")
    
    # Task Repository Configuration
    task_db_path: str = Field(default="memory/tasks.db", description="SQLite database path")
    task_auto_commit: bool = Field(default=True, description="Auto-commit transactions")
    
    # Monitoring Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/jarvis.log", description="Log file path")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    metrics_file: str = Field(default="logs/metrics.json", description="Metrics file path")
    enable_tracing: bool = Field(default=False, description="Enable request tracing")
    
    # Agent Configuration
    agent_timeout: int = Field(default=300, description="Agent execution timeout in seconds")
    agent_retry_attempts: int = Field(default=3, description="Number of retry attempts")
    agent_retry_delay: int = Field(default=5, description="Delay between retries in seconds")
    
    # System Configuration
    default_work_hours: float = Field(default=8.0, description="Default work hours per day")
    max_daily_tasks: int = Field(default=10, description="Maximum tasks per day")
    enable_ai_services: bool = Field(default=True, description="Enable AI services")
    enable_mock_mode: bool = Field(default=False, description="Use mock AI responses")
    
    def get_openai_config(self) -> dict:
        """Get OpenAI configuration as dictionary.
        
        Returns:
            Dictionary with OpenAI settings
        """
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "temperature": self.openai_temperature,
            "max_tokens": self.openai_max_tokens,
            "timeout": self.openai_timeout,
        }
    
    def get_memory_config(self) -> dict:
        """Get memory configuration as dictionary.
        
        Returns:
            Dictionary with memory settings
        """
        return {
            "base_path": self.memory_base_path,
            "type": self.memory_type,
            "auto_backup": self.memory_auto_backup,
            "backup_interval": self.memory_backup_interval,
        }
    
    def get_monitoring_config(self) -> dict:
        """Get monitoring configuration as dictionary.
        
        Returns:
            Dictionary with monitoring settings
        """
        return {
            "log_level": self.log_level,
            "log_file": self.log_file,
            "log_format": self.log_format,
            "enable_metrics": self.enable_metrics,
            "metrics_file": self.metrics_file,
            "enable_tracing": self.enable_tracing,
        }
    
    def is_production(self) -> bool:
        """Check if running in production mode.
        
        Returns:
            True if not in debug mode
        """
        return not self.api_debug
    
    def validate_settings(self) -> None:
        """Validate critical settings.
        
        Raises:
            ValueError: If critical settings are invalid
        """
        if self.enable_ai_services and not self.enable_mock_mode and not self.openai_api_key:
            raise ValueError(
                "OpenAI API key is required when AI services are enabled "
                "and mock mode is disabled"
            )
        
        if self.default_work_hours <= 0 or self.default_work_hours > 24:
            raise ValueError("Default work hours must be between 0 and 24")
        
        if self.max_daily_tasks <= 0:
            raise ValueError("Max daily tasks must be positive")


# Global settings instance
settings = Settings()
