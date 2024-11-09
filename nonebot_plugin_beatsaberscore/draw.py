from PIL import Image, ImageDraw, ImageFilter
import httpx
import base64
from io import BytesIO
from . import retry, loading_font, corner, calculation
from nonebot.log import logger
from pathlib import Path

async def draw_image(scores_total,player_total,old_data,cache_dir,cache_file,SS = False):
    avatar = await player_image(player_total)
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
    player_name = player_total['name']
    if len(player_total['name']) >= int(15):
        player_name = player_total['name'][:10] + '..'
    else:
        pass
    player_info = [
        {'text': player_name, 'position': (720, 80), 'font_size': 120, 'color': (255, 255, 255)},  # 玩家名称
        {'text': f"{player_total['total_pp']}PP", 'position': (720, 210), 'font_size': 100, 'color': (255, 105, 180)},  # 总PP
        {'text': f"Top PP:{player_total['top_pp']}", 'position': (720, 320), 'font_size': 90, 'color': (255, 255, 255)},  # 最高PP
        {'text': f"Global Rank:{player_total['player_rank']}", 'position': (720, 440), 'font_size': 90, 'color': (255, 255, 255)},  # 全球排名
        {'text': f"Country Rank:{player_total['player_country_rank']}", 'position': (720, 560), 'font_size': 90, 'color': (255, 255, 255)},  # 国家排名
    ]

    for player in player_info:
        font_size = player['font_size']
        font_player = 'HanYi'
        font = loading_font.font_loader(font_size = font_size, font = font_player)

        bs_draw.text(player['position'], player['text'], font=font, fill=player['color'])

    # 排行榜图标
    rankings_image_size = avatar_size # 先给图片赋值防止报错
    if SS == True:
        rankings_image = Image.open(f'{Path(__file__).parent}/static/ScoreSaber/scoresaber.png').convert('RGBA')
        rankings_image_size = (700, 700)
    else:
        rankings_image = Image.open(f'{Path(__file__).parent}/static/BeatLeader/beatleader.png').convert('RGBA')
        rankings_image_size = (620, 620)

    rankings_image = rankings_image.resize(rankings_image_size)
    beatleader_position = (3200, 90)
    background_image.paste(rankings_image, beatleader_position, rankings_image)

    start_x_offset = background_offset_x = start_background_offset_x = 110
    start_y_position = background_offset_y = 1700
    image_size = (310, 310)  # 图像大小
    if scores_total == 114514:
        return
    elif scores_total == 1919810:
        return
    song_image_urls = scores_total.get('song_image_url', [])

    i = 0
    # 处理歌曲背景图和歌曲图像
    for total_song in song_image_urls:
        crop_size = (100, 200, 900, 600)
        song_image = await download_image(total_song)
        # 处理歌曲背景
        if song_image:
            # 新的歌曲背景板
            open_blank = Image.open(f'{Path(__file__).parent}/static/blank.png').convert('RGBA')
            copy_blank = open_blank.copy()
            song_background_size = (920, 420)
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
        else:
            pass
        position = calculation.calculate_position(record = i,change = crop_size[2])
        # 处理歌曲图片
        if song_image:
            song_image = song_image.convert('RGBA')
            handle_image = corner.handle_corn(image = song_image, size = image_size, corner_radius = 25)
            mask_song_image = handle_image.convert('RGBA')
            background_image.paste(mask_song_image, (position[0], position[1]), mask_song_image)
            # 利用歌曲背景长度计算图片间隔
        else:
            pass
        i += 1
    logger.info('歌曲图片全部处理完毕')

    i = 0
    # 歌曲名称
    for name in scores_total['song_name']:
        position = calculation.calculate_position(record = i,change = crop_size[2])
        # 长名字适当缩短
        if len(name) > int(15):
            name = name[:12] + '..'
        else:
            pass
        
        name_size = 60
        font_song = loading_font.font_loader(font_size = name_size)
        bs_draw.text(((position[0] + image_size[0] + 18), position[1] - 25), name, font=font_song, fill=(255, 255, 255))
        i += 1

    i = 0
    # 歌曲id
    open_id_icon = Image.open(f'{Path(__file__).parent}/static/id.png').convert('RGBA')
    for song_id in scores_total['song_id']:
        position = calculation.calculate_position(record = i,change = crop_size[2])
        # id图标
        copy_id_icon = open_id_icon.copy()
        id_icon_size = (50, 50)
        copy_id_icon = copy_id_icon.resize(id_icon_size)
        background_image.paste(copy_id_icon, (position[0] + image_size[0] + 10, position[1] + id_icon_size[1] - 15), copy_id_icon)
        # 删除掉api响应中莫名其妙的xxx,确保map id是正确的
        song_id = song_id.replace('x', '')
        id_size = 50
        id_font = loading_font.font_loader(font_size = id_size)
        bs_draw.text((position[0] + image_size[0] + id_icon_size[0] + 10, position[1] + id_size - 7), str(song_id), font=id_font, fill=(123, 209, 225))
        # 歌曲数
        number_size = 55
        font_number = loading_font.font_loader(font_size = number_size)
        bs_draw.text((position[0] + image_size[0] + id_icon_size[0] + 370, position[1] + number_size - 15), f'#{(i + 1)}', font=font_number, fill=(123, 209, 225))
        i += 1

    # 权重数据
    song_weight = [float(song_weight) for song_weight in scores_total['song_weight']]
    # 歌曲PP数据
    song_pp_group = [float(pp) for pp in scores_total['song_pp']]
    # 歌曲PP & 权重PP绘制
    i = 0
    for song_pp in scores_total['song_pp']:
        position = calculation.calculate_position(record = i,change = crop_size[2])
        # PP信息
        pp_size = 70
        font_pp = loading_font.font_loader(font_size = pp_size)
        # 计算权重
        pp_weight_calculate = str(str(f'{(song_pp_group[i] * song_weight[i]):.2f}'))
        bs_draw.text((position[0] + image_size[0] + 10, position[1] + id_icon_size[1] + 45), str(f'{song_pp:.2f}>>{pp_weight_calculate}'), font=font_pp, fill=(94, 255, 223))
        i += 1
            
    open_acc_icon = Image.open(f'{Path(__file__).parent}/static/accuracy.png').convert('RGBA')
    open_acc_rank_ss_plus = Image.open(f'{Path(__file__).parent}/static/rank/ss_plus.png').convert('RGBA')
    open_acc_rank_ss = Image.open(f'{Path(__file__).parent}/static/rank/ss.png').convert('RGBA')
    open_acc_rank_s = Image.open(f'{Path(__file__).parent}/static/rank/s.png').convert('RGBA')
    open_acc_rank_a = Image.open(f'{Path(__file__).parent}/static/rank/a.png').convert('RGBA')
    # 准度绘制
    i = 0
    for accuracy in scores_total['song_accuracy']:
        position = calculation.calculate_position(record = i,change = crop_size[2])
        # acc图标
        copy_acc_icon = open_acc_icon.copy()
        acc_icon_size = (110, 110)
        copy_acc_icon = copy_acc_icon.resize(acc_icon_size)
        background_image.paste(copy_acc_icon, (position[0] + image_size[0] + 10, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + 110), copy_acc_icon)
        # 准度
        accuracy = round(float(accuracy * int(100)), 2)
        accuracy_size  = 70
        accuracy_font = loading_font.font_loader(font_size = accuracy_size)
        bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + 10, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + 110), (str(accuracy) + '%'), font=accuracy_font, fill=(255, 255, 255))
        i += 1

        # 准度评级
        acc_rank_icon_size = (230, 230)
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
        if int(80) > accuracy >= int(70):
            copy_acc_rank_a = open_acc_rank_a.copy()
            copy_acc_rank_a = copy_acc_rank_a.resize(acc_rank_icon_size)
            copy_acc_rank_icon = copy_acc_rank_a

        background_image.paste(copy_acc_rank_icon, (position[0] + image_size[0] + acc_icon_size[0] + 220, (int(position[1]) + (int(name_size))) + 100), copy_acc_rank_icon)
    

    i = 0
    # acc提升绘制
    if SS != True:
        for improve_acc in scores_total['improve_acc']:
            position = calculation.calculate_position(record = i,change = crop_size[2])
            improve_acc = round(float(improve_acc * int(100)), 2)
            improve_size = 25
            improve_acc__font = loading_font.font_loader(font_size = improve_size)
            bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + 240, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + 105), str( '(+' + str(improve_acc) + '%)'), font=improve_acc__font, fill=(255, 255, 255))
            i += 1
    else:
        # ScoreSaber获取不到这个数据,之后可能会结合本地文件去计算
        pass

    # 左/右手准度
    i = 0
    if SS != True:
        for song_accleft in scores_total['song_accleft']:
            song_accright = [song_accright for song_accright in scores_total['song_accright']]
            position = calculation.calculate_position(record = i,change = crop_size[2])
            hand_left = f'{float(song_accleft):.2f}'
            left_and_right_size = 40
            # 左手准度
            left_and_right_font = loading_font.font_loader(font_size = left_and_right_size)
            bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] - 10, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + int(left_and_right_size) + 140), str(hand_left), font=left_and_right_font, fill=(255, 51, 51))
            # 小分割线
            bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + (left_and_right_size * 3) - 5, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + int(left_and_right_size) + 140), '|', font=left_and_right_font, fill=(255, 255, 255))
            # 右手准度
            hand_right = f'{float(song_accright[i]):.2f}'
            bs_draw.text((position[0] + image_size[0] + acc_icon_size[0] + left_and_right_size + 90, (int(position[1]) + (int(name_size) + int(id_size)) // 2) + int(left_and_right_size) + 140), str(hand_right), font=left_and_right_font, fill=(100, 103, 254))
            i += 1
    else:
        # 不给数据+1
        pass
    
    song_stars = scores_total['song_stars']
    song_difficulty = scores_total.get('song_difficulty', [])
    i = 0
    for difficulty in song_difficulty:
        position = calculation.calculate_position(record = i,change = crop_size[2])
        difficulty_icon_size = (400, 400)
        # 星评难度图标
        if SS == True:
            open_difficulty_icon = Image.open(f'{Path(__file__).parent}/static/ScoreSaber/{difficulty}.png').convert('RGBA')
        else:
            open_difficulty_icon = Image.open(f'{Path(__file__).parent}/static/BeatLeader/{difficulty}.png').convert('RGBA')
        copy_difficulty_icon = open_difficulty_icon.copy()
        copy_difficulty_icon = copy_difficulty_icon.resize(difficulty_icon_size)
        background_image.paste(copy_difficulty_icon, (position[0] - (image_size[0] // 2) + 20,  position[1] - (image_size[1] // 2) - 20), copy_difficulty_icon)

        # 绘制星评
        difficulty_size = 35
        font_difficulty = loading_font.font_loader(font_size = difficulty_size, font = 'Teko-Bold')
        difficulty_star = song_stars
        bs_draw.text((position[0] + difficulty_size + 3, position[1]), str(f'{difficulty_star[i]:.2f}'), font=font_difficulty, fill=(255, 255, 225))
        i += 1
    
    '''
    # 歌曲变更高亮显示
    new_id_data = scores_total['song_id']
    new_pp_data = scores_total['song_pp']
    old_id_data = old_data['id_data']
    old_pp_data = old_data['id_data']
    result_data = calculation.contrast(new_id_data,new_pp_data,old_id_data,old_pp_data)
    open_highlight_icon = Image.open(f'{Path(__file__).parent}/static/highlight.png').convert('RGBA')
    for record in result_data:
        copy_highlight_icon = open_highlight_icon.copy()
        # 引用一下背景图大小
        highlight_size = song_background_size
        copy_highlight_icon = copy_highlight_icon.resize(highlight_size)
    
        highlight_position = calculation.calculate_position(record,start_x_offset,start_y_position,change = crop_size[2])
        background_image.paste(copy_highlight_icon, highlight_position, copy_highlight_icon)
    '''
    # 做点标记
    project_size = 80
    font_difficulty = loading_font.font_loader(font_size = project_size)
    information = str('nonebot-plugin-beatsaberscore By qwq12738qwq')
    bs_draw.text(((background_image_size[0] // 2) - len(information) - 950, background_image_size[1] - project_size), information, font=font_difficulty, fill=(44, 106, 163))

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
            except IOError:
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
            except IOError:
                return None
        except httpx.RequestError:
            return None