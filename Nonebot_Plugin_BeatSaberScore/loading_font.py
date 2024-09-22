from PIL import ImageFont
from pathlib import Path

def font_loader(font_size, font_name = None):
    font_path = f'{Path(__file__).parent}/static/Teko-Bold.ttf'
    if font_name == None:
        pass
    else:
        font_path = font_name
    try:
        loaded_font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f'无法加载字体文件 {font_path}. 使用默认字体。')
        loaded_font = ImageFont.load_default()
    return loaded_font