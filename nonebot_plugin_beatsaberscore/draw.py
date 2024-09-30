from PIL import Image, ImageDraw, ImageFilter
import httpx
import base64
from io import BytesIO
from . import retry
from . import loading_font
from . import corner
from nonebot.log import logger
from pathlib import Path

async def draw_image(scores_total,player_total,cache_dir,cache_file):
    avatar = await player_image(player_total)
    if avatar is None:
        return 114514
    avatar = avatar.convert("RGBA")
    background_image = Image.open(f'{Path(__file__).parent}/static/bg.png').convert('RGBA')
    # 更改头像图片大小
    avatar_size = (300, 300)
    round_avatar = corner.handle_corn(image = avatar, size = avatar_size, corner_radius = 30)
    # 列表[0]宽,[1]高
    background_image_size = background_image.size
    avatar_position = (1490, 90)

    bs_draw = ImageDraw.Draw(background_image)
    background_image.paste(round_avatar, avatar_position, round_avatar)
    player_name = player_total['name']
    if len(player_total['name']) >= int(9):
        player_name = player_total['name'][:7] + '..'
    else:
        pass
    player_info = [
        {'text': player_name, 'position': (1820, 80), 'font_size': 80, 'color': (255, 255, 255)},  # 玩家名称
        {'text': f"{player_total['total_pp']}PP", 'position': (1820, 180), 'font_size': 70, 'color': (255, 105, 180)},  # 总PP
        {'text': f"Top PP:{player_total['top_pp']}", 'position': (1820, 250), 'font_size': 50, 'color': (255, 255, 255)},  # 最高PP
        {'text': f"Global Rank:{player_total['player_rank']}", 'position': (1820, 350), 'font_size': 50, 'color': (255, 255, 255)},  # 全球排名
        {'text': f"Country Rank:{player_total['player_country_rank']}", 'position': (1820, 300), 'font_size': 50, 'color': (255, 255, 255)},  # 国家排名
    ]

    for player in player_info:
        font_size = player['font_size']
        font_path = f'{Path(__file__).parent}/static/HanYi.ttf'
        font = loading_font.font_loader(font_size, font_path)

        bs_draw.text(player['position'], player['text'], font=font, fill=player['color'])

    # beatleader图标
    beatleader_image = Image.open(f'{Path(__file__).parent}/static/beatleader.png').convert('RGBA')
    beatleader_image = beatleader_image.resize(avatar_size)
    beatleader_position = (2350, 90)
    background_image.paste(beatleader_image, beatleader_position, beatleader_image)

    x_song_image = start_x_offset = background_offset_x = start_background_offset_x = x_name_position = x_acc_position = x_acc_icon = x_pp = x_pp_weight = x_acc_improve = x_song_id = x_difficulty = 100
    y_song_image = background_offset_y = y_name_position = y_acc_position = y_acc_icon = y_pp = y_pp_weight = y_acc_improve = y_song_id = y_difficulty = 500
    image_size = (320, 320)  # 图像大小
    if scores_total == 114514:
        return
    elif scores_total == 1919810:
        return
    song_image_urls = scores_total.get('song_image_url', [])
    # 处理歌曲背景图和歌曲图像
    for total_song in song_image_urls:
        song_image = await download_image(total_song)
        # 处理歌曲背景
        if song_image:
            song_background = song_image.copy()
            expand_size = (1000, 1000)
            song_background = song_background.resize(expand_size)
            # crop(left, upper, right, lower)
            crop_size = (100, 200, 900, 600)
            song_background_size = (crop_size[2] - crop_size[0], crop_size[3] - crop_size[1])
            song_background_length = int(crop_size[2] - crop_size[0])
            song_background = song_background.crop(crop_size)
            handle_SB = song_background.convert('RGBA')
            handle_SB = corner.handle_corn(image = song_background, size = song_background_size, corner_radius = 25)
            song_background = handle_SB.convert('RGBA')
            open_acrylic = Image.open(f'{Path(__file__).parent}/static/acrylic.png').convert('RGBA')
            background_acrylic = open_acrylic.copy()
            # 图片高斯模糊
            song_background = song_background.filter(ImageFilter.GaussianBlur(6))
            # 处理图片圆角
            background_acrylic = background_acrylic.resize(song_background_size)
            song_background = Image.alpha_composite(song_background, background_acrylic)
            background_image.paste(song_background, (background_offset_x, background_offset_y), song_background)
            background_offset_x += int(song_background_length + 200)  # 位置间隔调整
            if background_offset_x >= 4000:
                background_offset_y += 650
                background_offset_x = start_background_offset_x
            else:
                pass
        else:
            pass
        # 处理歌曲图片
        if song_image:
            song_image = song_image.convert('RGBA')
            handle_image = corner.handle_corn(image = song_image, size = image_size, corner_radius = 25)
            mask_song_image = handle_image.convert('RGBA')
            background_image.paste(mask_song_image, (x_song_image, y_song_image), mask_song_image)
            # 利用歌曲背景长度计算图片间隔
            x_song_image += crop_size[2] + 100
            if x_song_image > 3200:
                y_song_image += 650
                x_song_image = start_x_offset
            else:
                pass
    logger.info('歌曲图片全部处理完毕')

    # 歌曲名称
    for name in scores_total['song_name']:

        # 长名字适当缩短
        if len(name) > int(12):
            name = name[:10] + '...'
        else:
            pass
        
        name_size = 85
        font_song = loading_font.font_loader(font_size = name_size)

        bs_draw.text(((x_name_position + image_size[0] + 18), y_name_position - 25), name, font=font_song, fill=(144, 238, 255))

        x_name_position += crop_size[2] + 100  # 位置间隔调整
        if x_name_position > 3600:
            y_name_position += 650
            x_name_position = start_x_offset
        else:
            pass

    # 歌曲PP绘制
    for song_pp in scores_total['song_pp']:
        # PP图标
        open_pp_icon = Image.open(f'{Path(__file__).parent}/static/pp.png').convert('RGBA')
        copy_pp_icon = open_pp_icon.copy()
        pp_icon_size = (60, 60)
        copy_pp_icon = copy_pp_icon.resize(pp_icon_size)
        background_image.paste(copy_pp_icon, (x_pp + image_size[0] + 10, y_pp + pp_icon_size[1] + 15), copy_pp_icon)
        # PP信息
        pp_size = 85
        font_pp = loading_font.font_loader(font_size = pp_size)

        bs_draw.text((x_pp + image_size[0] + pp_icon_size[0] + 10, y_pp + 50), str(f'{song_pp:.2f}'), font=font_pp, fill=(255, 105, 180))
        x_pp += crop_size[2] + 100  # 位置间隔调整
        if x_pp > 3600:
            y_pp += 650
            x_pp = x_pp_weight = start_x_offset

        else:
            pass

    # 歌曲权重PP绘制
    song_pp_group = [float(pp) for pp in scores_total['song_pp']]
    for song_weight in scores_total['song_weight']:

        i = -1 + 1
        pp_weight = str('(' + str(f'{(song_pp_group[i] * song_weight):.2f}') + ')')
        # 保留小数点后两位
        weight_size = 50
        font_weight = loading_font.font_loader(font_size = weight_size)

        bs_draw.text((x_pp_weight + image_size[0] + 20, (int(y_pp_weight) + (int(name_size) + int(pp_size)) // 2) + 40), str(pp_weight), font=font_weight, fill=(255, 255, 255))
        x_pp_weight += crop_size[2] + 100
        if x_pp_weight > 3600:
            y_pp_weight += 650
            y_pp += 650
            x_pp_weight = start_x_offset
            

    # 准度绘制
    for accuracy in scores_total['song_accuracy']:
        # acc图标
        open_acc_icon = Image.open(f'{Path(__file__).parent}/static/accuracy.png').convert('RGBA')
        copy_acc_icon = open_acc_icon.copy()
        acc_icon_size = (60, 60)
        copy_acc_icon = copy_acc_icon.resize(acc_icon_size)
        background_image.paste(copy_acc_icon, (x_acc_icon + image_size[0] + 10, (int(y_acc_icon) + (int(name_size) + int(pp_size) + int(weight_size)) // 2) + 70), copy_acc_icon)
        # 准度
        accuracy = round(float(accuracy * int(100)), 2)
        accuracy_size  = 80
        accuracy_font = loading_font.font_loader(font_size = accuracy_size)
        bs_draw.text((x_acc_position + image_size[0] + acc_icon_size[0] + 10, (int(y_acc_position) + (int(name_size) + int(pp_size) + int(weight_size)) // 2) + 50), (str(accuracy) + '%'), font=accuracy_font, fill=(255, 255, 255))
        x_acc_position += crop_size[2] + 100
        x_acc_icon = x_acc_position
        if x_acc_position > 3600:
            x_acc_position = x_acc_icon = start_x_offset
            y_acc_position += 650
            y_acc_icon = y_acc_position
        else:
            pass
    
    # acc提升绘制图片
    for improve_acc in scores_total['improve_acc']:
        improve_acc = round(float(improve_acc * int(100)), 2)
        improve_size = 60
        improve_acc__font = loading_font.font_loader(font_size = improve_size)
        bs_draw.text((x_acc_improve + image_size[0] + 20, (int(y_acc_improve) + (int(name_size) + int(pp_size) + int(weight_size) + int(accuracy_size)) // 2) + 80), str( '(+' + str(improve_acc) + '%)'), font=improve_acc__font, fill=(144, 238, 144))
        x_acc_improve += crop_size[2] + 100
        if x_acc_improve > 3600:
            x_acc_improve = start_x_offset
            y_acc_improve +=  650
        else:
            pass
    # 歌曲id
    y_song_id += crop_size[3] - crop_size[1]
    for song_id in scores_total['song_id']:
        # id图标
        open_id_icon = Image.open(f'{Path(__file__).parent}/static/id.png').convert('RGBA')
        copy_id_icon = open_id_icon.copy()
        id_icon_size = (80, 80)
        copy_id_icon = copy_id_icon.resize(id_icon_size)
        background_image.paste(copy_id_icon, (x_song_id, int(y_song_id) + (image_size [1] - (crop_size[3] - crop_size[1]))), copy_id_icon)
        # 删除掉api响应中莫名其妙的xxx,确保map id是正确的
        song_id = song_id.replace('x', '')
        id_size = 90
        id_font = loading_font.font_loader(font_size = id_size)
        bs_draw.text((x_song_id + id_icon_size[0], int(y_song_id) + (image_size [1] - (crop_size[3] - crop_size[1])) - 20), str(song_id), font=id_font, fill=(123, 209, 225))

        x_song_id += crop_size[2] + 100
        if x_song_id > 3600:
            x_song_id = start_x_offset
            y_song_id += 650
        else:
            pass

    song_stars = scores_total['song_stars']
    song_difficulty = scores_total.get('song_difficulty', [])
    i = -1
    for difficulty in song_difficulty:
        difficulty_icon_size = (180, 150)
        # 判断难度
        if difficulty == 'Easy':
            open_easy_icon = Image.open(f'{Path(__file__).parent}/static/easy.png').convert('RGBA')
            copy_easy_icon = open_easy_icon.copy()
            copy_easy_icon = copy_easy_icon.resize(difficulty_icon_size)
            background_image.paste(copy_easy_icon, (x_difficulty + image_size[0] - difficulty_icon_size[0],  y_difficulty + image_size[1] - difficulty_icon_size[1]), copy_easy_icon)
        elif difficulty == 'Normal':
            open_normal_icon = Image.open(f'{Path(__file__).parent}/static/normal.png').convert('RGBA')
            copy_normal_icon = open_normal_icon.copy()
            copy_normal_icon = copy_normal_icon.resize(difficulty_icon_size)
            background_image.paste(copy_normal_icon, (x_difficulty + image_size[0] - difficulty_icon_size[0],  y_difficulty + image_size[1] - difficulty_icon_size[1]), copy_normal_icon)
        elif difficulty == 'Hard':
            open_hard_icon = Image.open(f'{Path(__file__).parent}/static/hard.png').convert('RGBA')
            copy_hard_icon = open_hard_icon.copy()
            copy_hard_icon = copy_hard_icon.resize(difficulty_icon_size)
            background_image.paste(copy_hard_icon, (x_difficulty + image_size[0] - difficulty_icon_size[0],  y_difficulty + image_size[1] - difficulty_icon_size[1]), copy_hard_icon)
        elif difficulty == 'Expert':
            open_expert_icon = Image.open(f'{Path(__file__).parent}/static/expert.png').convert('RGBA')
            copy_expert_icon = open_expert_icon.copy()
            copy_expert_icon = copy_expert_icon.resize(difficulty_icon_size)
            background_image.paste(copy_expert_icon, (x_difficulty + image_size[0] - difficulty_icon_size[0],  y_difficulty + image_size[1] - difficulty_icon_size[1]), copy_expert_icon)
        elif difficulty == 'ExpertPlus':
            open_expertplus_icon = Image.open(f'{Path(__file__).parent}/static/expertplus.png').convert('RGBA')
            copy_expertplus_icon = open_expertplus_icon.copy()
            copy_expertplus_icon = copy_expertplus_icon.resize(difficulty_icon_size)
            background_image.paste(copy_expertplus_icon, (x_difficulty + image_size[0] - difficulty_icon_size[0],  y_difficulty + image_size[1] - difficulty_icon_size[1]), copy_expertplus_icon)
        else:
            pass
        # 绘制星评
        difficulty_size = 50
        font_difficulty = loading_font.font_loader(font_size = difficulty_size)
        difficulty_star = song_stars
        i += 1
        bs_draw.text((x_difficulty + image_size[0] - difficulty_size // 2 - 80, y_difficulty + image_size [1] - difficulty_size - 55), str(f'{difficulty_star[i]:.2f}'), font=font_difficulty, fill=(255, 255, 225))

        x_difficulty += crop_size[2] + 100
        if x_difficulty > 3600:
                x_difficulty = start_x_offset
                y_difficulty += 650
        else:
            pass
        
        # 做点标记
        project_size = 80
        font_difficulty = loading_font.font_loader(font_size = project_size)
        information = str('nonebot-plugin-beatsaberscore By qwq12738qwq')
        bs_draw.text(((background_image_size[0] // 2) - len(information) * project_size, background_image_size[1] - project_size), information, font=font_difficulty, fill=(44, 106, 163))

    background_image.save(f'{cache_dir}/BS_cache.png')
    with open(cache_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

async def player_image(player_total):
    player_avatar = player_total['player_avatar']
    async with httpx.AsyncClient():
        get_avatar = await retry.time_out_retry(url = player_avatar)
        if get_avatar == None:
            return
        try:
            avatar_data = BytesIO(get_avatar.content)
            try:
                # 尝试打开图像数据
                return Image.open(avatar_data)
            except IOError as e:
                return None
        except httpx.RequestError:
            return None

async def download_image(image_url):
    async with httpx.AsyncClient():
        get_song_image = await retry.time_out_retry(url = image_url)
        if get_song_image == None:
            return
        else:
            pass
        
        try:
            song_data = BytesIO(get_song_image.content)
            try:
                return Image.open(song_data)
            except IOError as e:
                return None
        except httpx.RequestError:
            return None