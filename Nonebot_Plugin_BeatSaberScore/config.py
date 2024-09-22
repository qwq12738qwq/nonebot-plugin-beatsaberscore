from pydantic import BaseModel

class Config(BaseModel):
    BS_retries: int = 8
    BS_timeout: int = 5
config = Config()