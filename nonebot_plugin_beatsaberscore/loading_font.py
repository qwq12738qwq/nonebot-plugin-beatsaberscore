from PIL import ImageFont
from pathlib import Path
from nonebot.log import logger

async def font_loader(font_size, font_name = None, font = 'arial-bold'):
    font_path = f'{Path(__file__).parent}/static/ttf/{font}.ttf'
    if font_name == None:
        pass
    else:
        font_path = font_name
    try:
        loaded_font = ImageFont.truetype(font_path, font_size)
    except IOError:
        logger.error(f'无法加载字体文件 {font_path},请检查插件是否完整,或者重装插件,如果还有报错,请到github提出issues')
        loaded_font = ImageFont.load_default()
    return loaded_font