import httpx
import asyncio
from .config import BS_RETRIES, BS_TIMEOUT
from nonebot.log import logger

async def time_out_retry(url, retries = BS_RETRIES, timeout = BS_TIMEOUT, params = None):
    attempt = 0
    while attempt < retries:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=timeout, params = params)
                response.raise_for_status()
                return response
        except (httpx.RequestError, httpx.HTTPStatusError):
            attempt += 1
            if attempt == retries // 2:
                logger.warning(f'重试网络达到{retries}次,请注意网络状态')
                if attempt == retries:
                    logger.error(f'重试网络达到{retries}次,请尝试在env.prod文件中调大重试次数或者检查本地网络配置')
                    return None
                else:
                    wait_time = int(2)
                    await asyncio.sleep(wait_time)