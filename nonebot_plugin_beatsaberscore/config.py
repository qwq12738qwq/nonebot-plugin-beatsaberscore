from pydantic import BaseModel
from nonebot import get_plugin_config
from pydantic import BaseModel, Field

class Config(BaseModel):
    # 配置项
    bs_retries: int = Field(default=8)
    bs_timeout: int = Field(default=5)
    superusers: list = Field(default=None)
    bs_limit_cache: int = Field(default=1500)
    version: str = '1.3.7'

plugin_config: Config = get_plugin_config(Config)
# 读取配置项
BS_RETRIES = plugin_config.bs_retries
BS_TIMEOUT = plugin_config.bs_timeout
SUPERUSERS = plugin_config.superusers
BS_LIMIT_CACHE = plugin_config.bs_limit_cache
VERSION = plugin_config.version