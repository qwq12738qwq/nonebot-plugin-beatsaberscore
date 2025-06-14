import os
import json
from pathlib import Path
from .config import BS_LIMIT_CACHE
from nonebot.log import logger


async def cache_manager(cache_file_path):
    Data_Path = Path(f"{cache_file_path}") / "cache_data.json"
    if Data_Path.exists():
        with open(Data_Path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        if cache_data == {}:
            return False
        else:
            image_number = int(len(os.listdir(cache_file_path)))
            if image_number > BS_LIMIT_CACHE:
                pass
            else:
                return False
    else:
        return False

    Tidy_Data = sorted(cache_data.items(), key=lambda item: item[1])
    Over_Cache = int(image_number - BS_LIMIT_CACHE)
    i = 0
    while i < Over_Cache:
        Clean_Name = str(Tidy_Data[1500+i][1])
        os.remove(f"{Path(cache_file_path)}/{Clean_Name}.png")
        i = i+1
    logger.info(f"缓存清理工作完成,共清理{image_number - BS_LIMIT_CACHE}张缓存图片")
    return True



    