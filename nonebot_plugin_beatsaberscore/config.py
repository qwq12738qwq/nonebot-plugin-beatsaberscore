from pydantic import BaseModel
from nonebot import get_plugin_config
from pydantic import BaseModel, Field

class Config(BaseModel):
    # 配置项
    bs_retries: int = Field(default=8)
    bs_timeout: int = Field(default=5)

plugin_config: Config = get_plugin_config(Config)
# 读取配置项
BS_RETRIES = plugin_config.bs_retries
BS_TIMEOUT = plugin_config.bs_timeout