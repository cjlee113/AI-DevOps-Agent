from pydantic import BaseSettings

class Settings(BaseSettings):
    GITHUB_APP_TOKEN: str  # fine-grained PAT or App installation token
    GITHUB_WEBHOOK_SECRET: str
    OPENAI_API_KEY: str | None = None
    RUN_TESTS: bool = True
    AGENT_MODE: str = "simple"  # "simple" | "langchain"
    
    class Config:
        env_file = ".env"


settings = Settings()