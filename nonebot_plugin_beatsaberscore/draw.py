from PIL import Image, ImageDraw
import httpx
import asyncio
import base64
from io import BytesIO
from . import retry, loading_font, corner, calculation, storage
from nonebot.log import logger
from pathlib import Path
from .config import BS_FAST_DOWNLOAD

async def draw_image(Ranks_datas,old_data,cache_dir,cache_file,data_dir,SS = False):
    avatar = await player_image(player_addr = f"{Ranks_datas['player']['player_avatar']}")
    if avatar is None:
        return 114514
    avatar = avatar.convert("RGBA")
    background_image = Image.open(f'{Path(__file__).parent}/static/bg.png').convert('RGBA')
    # 更改头像图片大小
    avatar_size = (600, 600)
    round_avatar = corner.handle_corn(image = avatar, size = avatar_size, corner_radius = 30)
    # 列表[0]宽,[1]高
    background_image_size = background_image.size
    avatar_position = (100, 90)

    bs_draw = ImageDraw.Draw(background_image)
    background_image.paste(round_avatar, avatar_position, round_avatar)
    player_name = Ranks_datas['player']['player_name']
    if len(Ranks_datas['player']['player_name']) >= int(15):
        player_name = Ranks_datas['player']['player_name'][:10] + '..'
    else:
        pass
    player_info = [
        {'text': player_name, 'position': (720, 80), 'font_size': 120, 'color': (255, 255, 255)},  # 玩家名称
        {'text': f"{Ranks_datas['player']['player_pp']}PP", 'position': (720, 210), 'font_size': 100, 'color': (255, 105, 180)},  # 总PP
        {'text': f"Person Stars:{(float(Ranks_datas['player']['player_stars'])):.2f}", 'position': (720, 320), 'font_size': 90, 'color': (255, 255, 255)},  # 最高PP
        {'text': f"Global Rank:{Ranks_datas['player']['player_rank']}", 'position': (720, 440), 'font_size': 90, 'color': (255, 255, 255)},  # 全球排名
        {'text': f"Country Rank:{Ranks_datas['player']['player_country_rank']}", 'position': (720, 560), 'font_size': 90, 'color': (255, 255, 255)},  # 国家排名
    ]

    for player in player_info:
        font_size = player['font_size']
        font = await loading_font.font_loader(font_size = font_size, font = 'HanYi')

        bs_draw.text(player['position'], player['text'], font=font, fill=player['color'])
    if old_data != {}:
        old_star = float(old_data['player']['player_stars'])
        old_pp = float(old_data['player']['player_pp'])
        if float(Ranks_datas['player']['player_stars']) - float(old_star) < 0:
            old_star = float(Ranks_datas['player']['player_stars'])
            old_pp = float(Ranks_datas['player']['player_pp'])
    else:
        old_star = float(Ranks_datas['player']['player_stars'])
        old_pp = float(Ranks_datas['player']['player_pp'])
    bs_draw.text((720 + int(len(player_info[2]['text'])) * 52, 320), f"+{(float(Ranks_datas['player']['player_stars']) - old_star):.2f}", font=font, fill=(69, 195, 40))
    bs_draw.text((720 + int(len(player_info[1]['text'])) * 65, 210), f"+{(float(Ranks_datas['player']['player_pp']) - old_pp):.2f}", font=font, fill=(69, 195, 40))
    # 排行榜图标
    rankings_image_size = avatar_size # 先给图片大小赋值防止报错
    if SS == True:
        rankings_image = Image.open(f'{Path(__file__).parent}/static/ScoreSaber/scoresaber.png').convert('RGBA')
        rankings_image_size = (700, 700)
    else:
        rankings_image = Image.open(f'{Path(__file__).parent}/static/BeatLeader/beatleader.png').convert('RGBA')
        rankings_image_size = (620, 620)

    rankings_image = rankings_image.resize(rankings_image_size)
    beatleader_position = (3200, 90)
    background_image.paste(rankings_image, beatleader_position, rankings_image)

    background_offset_x = start_background_offset_x = 110
    background_offset_y = 1700
    image_size = (310, 310)  # 图像大小
    if Ranks_datas == 114514:
        return
    elif Ranks_datas == 1919810:
        return

    open_blank = Image.open(f'{Path(__file__).parent}/static/blank.png').convert('RGBA')
    open_id_icon = Image.open(f'{Path(__file__).parent}/static/id.png').convert('RGBA')
    open_acc_icon = Image.open(f'{Path(__file__).parent}/static/accuracy.png').convert('RGBA')
    open_acc_rank_ss_plus = Image.open(f'{Path(__file__).parent}/static/rank/ss_plus.png').convert('RGBA')
    open_acc_rank_ss = Image.open(f'{Path(__file__).parent}/static/rank/ss.png').convert('RGBA')
    open_acc_rank_s = Image.open(f'{Path(__file__).parent}/static/rank/s.png').convert('RGBA')
    open_acc_rank_a = Image.open(f'{Path(__file__).parent}/static/rank/a.png').convert('RGBA')
    name_size = 60
    font_song = await loading_font.font_loader(font_size = name_size)
    id_size = 50
    id_font = await loading_font.font_loader(font_size = id_size)
    number_size = 55
    font_number = await loading_font.font_loader(font_size = number_size)
    pp_size = 70
    font_pp = await loading_font.font_loader(font_size = pp_size)
    accuracy_size  = 70
    accuracy_font = await loading_font.font_loader(font_size = accuracy_size)
    improve_size = 32
    improve_acc__font = await loading_font.font_loader(font_size = improve_size)
    difficulty_size = 35
    font_difficulty = await loading_font.font_loader(font_size = difficulty_size, font = 'Teko-Bold')
    left_and_right_size = 50
    left_and_right_font = await loading_font.font_loader(font_size = left_and_right_size)
    crop_size = (100, 200, 900, 600)
    song_background_size = (920, 420)
    id_icon_size = (50, 50)
    acc_icon_size = (110, 110)
    acc_rank_icon_size = (230, 230)

    for i in range(40):
        # 处理歌曲背景
        copy_blank = open_blank.copy()
        copy_blank = copy_blank.resize(song_background_size)
        background_image.paste(copy_blank, (background_offset_x, background_offset_y), copy_blank)
        # 用于计算位置
        song_background_length = int(song_background_size[0])
        background_offset_x += song_background_length + 50
        if background_offset_x >= 3800:
            background_offset_y += 550
            background_offset_x = start_background_offset_x
        else:
            pass

    i = 0
    Downloads_Fast = False
    for song_name,datas in Ranks_datas['songs'].items():
        # 删掉难度和单手标识
        song_name = song_name.replace(f"{datas['difficulty']}", '').replace('|', '').replace(f"{datas['id']}", '')
        # 位置计算
        position = await calculation.calculate_position(record = int(datas['position']),change = crop_size[2])
        # 下载歌曲图片
        if BS_FAST_DOWNLOAD == False:
            song_image = await download_image(total_song = datas['image_url'], cache_dir = cache_dir, save_name = datas['id'],data_dir = Path(data_dir),save_id = datas['id'])
        else:
            if Downloads_Fast != True:
                asyncio_download = []
                song_name_list = []
                for song_name,datas in Ranks_datas['songs'].items():
                    # (total_song = datas['image_url'], cache_dir = cache_dir, save_name = datas['id'],data_dir = Path(data_dir),save_id = datas['id'])
                    asyncio_download.append(download_image(total_song=datas['image_url'], cache_dir=cache_dir, save_name=datas['id'], data_dir=Path(data_dir), save_id=datas['id']))
                    song_name = song_name.replace(f"{datas['difficulty']}", '').replace('|', '')
                    song_name_list.append(song_name)
                Downloads_Result = await asyncio.gather(*asyncio_download)
                Downloads_Fast = True
            else:
                pass
        song_image = Downloads_Result[i]
        i += 1
        
        # 处理歌曲图片
        if song_image:
            song_image = song_image.convert('RGBA')
            handle_image = corner.handle_corn(image = song_image, size = image_size, corner_radius = 25)
            mask_song_image = handle_image.convert('RGBA')
            background_image.paste(mask_song_image, (position[0], position[1]), mask_song_image)
        else:
            pass
        # 歌曲名称
        if len(song_name) > int(15): # 长名字适当缩短
            song_name = song_name[:12] + '..'
        else:
            pass
        bs_draw.text(((position[0] + image_size[0] + 18), position[1] - 25), song_name, font=font_song, fill=(255, 255, 255))
        # id图标
        copy_id_icon = open_id_icon.copy()
        copy_id_icon = copy_id_icon.resize(id_icon_size)
        background_image.paste(copy_id_icon, (position[0] + image_size[0] + 10, position[1] + id_icon_size[1] - 15), copy_id_icon)
        # 删除掉api响应中莫名其妙的xxx,确保map id是正确的
        song_id = datas['id'].replace('x', '').strip()
        bs_draw.text((position[0] + image_size[0] + id_icon_size[0] + 10, position[1] + id_size - 7), str(song_id), font=id_font, fill=(123, 209, 225))
        # 歌曲数
        bs_draw.text((position[0] + image_size[0] + id_icon_size[0] + 450 - len(f"#{(int(datas['position']) + 1)}") * 25, position[1] + number_size - 15), f"#{(int(datas['position']) + 1)}", font=font_number, fill=(123, 209, 225))
        # PP信息
        pp_weight_calculate = str(str(f"{(float(datas['pp']) * float(datas['weight'])):.2f}")) # 计算权重
        bs_draw.text((position[0] + image_size[0] + 10, position[1] + id_icon_size[1] + 45), f"{float(datas['pp']):.2f}>>{pp_weight_calculate}", font=font_pp, fill=(94, 255, 223))
        # acc图标
        copy_acc_icon = open_acc_icon.copy()
        copy_acc_icon = copy_acc_icon.resize(acc_icon_size)
        background_image.paste(copy_acc_icon, (position[0] + image_size[0] + 10, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + 110), copy_acc_icon)
        # 准度
        accuracy = float(float(datas['accuracy']) * int(100))
        bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + 10, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + 110), (f'{(accuracy):.2f}' + '%'), font=accuracy_font, fill=(255, 255, 255))
        # 准度评级
        offset = (position[0] + image_size[0] + acc_icon_size[0] + 220, (int(position[1]) + (int(name_size))) + 90)
        if accuracy >= int(95):
            copy_acc_rank_ss_plus = open_acc_rank_ss_plus.copy()
            copy_acc_rank_ss_plus = copy_acc_rank_ss_plus.resize(acc_rank_icon_size)
            copy_acc_rank_icon = copy_acc_rank_ss_plus
        if int(95) > accuracy >= int(90):
            copy_acc_rank_ss = open_acc_rank_ss.copy()
            copy_acc_rank_ss = copy_acc_rank_ss.resize(acc_rank_icon_size)
            copy_acc_rank_icon = copy_acc_rank_ss
        if int(90) > accuracy >= int(80):
            copy_acc_rank_s = open_acc_rank_s.copy()
            copy_acc_rank_s = copy_acc_rank_s.resize(acc_rank_icon_size)
            copy_acc_rank_icon = copy_acc_rank_s
            offset = (position[0] + image_size[0] + acc_icon_size[0] + 250, (int(position[1]) + (int(name_size))) + 90)
        if int(80) > accuracy >= int(65):
            copy_acc_rank_a = open_acc_rank_a.copy()
            copy_acc_rank_a = copy_acc_rank_a.resize(acc_rank_icon_size)
            copy_acc_rank_icon = copy_acc_rank_a
            offset = (position[0] + image_size[0] + acc_icon_size[0] + 250, (int(position[1]) + (int(name_size))) + 90)
        background_image.paste(copy_acc_rank_icon, offset, copy_acc_rank_icon)
        # 准度提升  
        improve_acc = round(float(float(datas['improvement']) * int(100)), 2)
        bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + 240, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + 105), str( '(+' + str(improve_acc) + '%)'), font=improve_acc__font, fill=(255, 255, 255))
        hand_left = f"{float(datas['accleft']):.2f}"
        # 左手准度
        bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + 110 - len(f'{hand_left}') * 20 - 80, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + int(left_and_right_size) + 80), str(hand_left), font=left_and_right_font, fill=(255, 51, 51))
        # 小分割线
        bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + (left_and_right_size * 3) - 80, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + int(left_and_right_size) + 80), '|', font=left_and_right_font, fill=(255, 255, 255))
        # 右手准度
        hand_right = f"{float(datas['accright']):.2f}"
        bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + left_and_right_size + 90 - 80, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + int(left_and_right_size) + 80), str(hand_right), font=left_and_right_font, fill=(100, 103, 254))
        difficulty_icon_size = (400, 400)
        # 星评难度图标
        if SS == True:
            open_difficulty_icon = Image.open(f"{Path(__file__).parent}/static/ScoreSaber/{datas['difficulty']}.png").convert('RGBA')
        else:
            open_difficulty_icon = Image.open(f"{Path(__file__).parent}/static/BeatLeader/{datas['difficulty']}.png").convert('RGBA')
        copy_difficulty_icon = open_difficulty_icon.copy()
        copy_difficulty_icon = copy_difficulty_icon.resize(difficulty_icon_size)
        background_image.paste(copy_difficulty_icon, (position[0] - (image_size[0] // 2) + 20,  position[1] - (image_size[1] // 2) - 20), copy_difficulty_icon)
        # 绘制星评
        bs_draw.text((position[0] + difficulty_size + 3, position[1]), f"{float(datas['stars']):.2f}", font=font_difficulty, fill=(255, 255, 225))

        

    logger.info('图片绘制处理完毕')
    project_size = 80
    font_difficulty = await loading_font.font_loader(font_size = project_size, font = 'HanYi')
    information = str('nonebot-plugin-beatsaberscore By qwq12738qwq | 数据仅供参考,不代表实际能力')
    bs_draw.text(((background_image_size[0] // 2) - len(information) - 1600, background_image_size[1] - project_size), information, font=font_difficulty, fill=(44, 106, 163))
    if SS == True:
        background_image.convert("RGB").save(f'{cache_dir}/SS_cache.jpg', "JPEG", quality=15)
    else:
        background_image.convert("RGB").save(f'{cache_dir}/BS_cache.jpg', "JPEG", quality=15)
    with open(cache_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

async def player_image(player_addr):
    async with httpx.AsyncClient():
        get_avatar = await retry.time_out_retry(url = player_addr)
        if get_avatar == None:
            return
        try:
            avatar_data = BytesIO(get_avatar.content)
            try:
                return Image.open(avatar_data)
            except IOError:
                return None
        except httpx.RequestError:
            return None

async def download_image(total_song,cache_dir,save_name,data_dir,save_id):
    save_id = save_id.replace('x', '').strip()
    save_name = save_name.replace('x', '').strip()
    # 先尝试去打开缓存图片
    try:
        save_image = Image.open(f'{cache_dir}/{save_name}.png').convert('RGBA')
        storage.cache_data(save_id,data_path = data_dir)
        return save_image
    except:
        pass
    async with httpx.AsyncClient():
        get_song_image = await retry.time_out_retry(url = total_song)
        if get_song_image == None:
            return
        else:
            pass
        try:
            # 保存图片到缓存
            with open(f'{cache_dir}/{save_name}.png', "wb") as f:
                 f.write(get_song_image.content)
            song_data = BytesIO(get_song_image.content)
            try:
                return Image.open(song_data)
            except IOError:
                return None
        except httpx.RequestError:
            return None