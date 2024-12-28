import os
import re
import json
# import subprocess
# from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot import require
require('nonebot_plugin_localstore')
import nonebot_plugin_localstore as store
# require('nonebot_plugin_apscheduler')
# from nonebot_plugin_apscheduler import scheduler
from .config import Config, SUPERUSERS
from . import api, draw, storage, retry, calculation

__version__ = "1.3.2"
__plugin_meta__ = PluginMetadata(
    name="Beat Saber查分器",
    description="Nonebot2的节奏光剑查分插件,支持BeatLeader&ScoreSaber查分o((>ω< ))o",
    type="application",
    config=Config,
    usage="BL score, SS score, BS bind, BS help, calculation",
    homepage="https://github.com/qwq12738qwq/nonebot-plugin-beatsaberscore",
    supported_adapters={"~onebot.v11"},
)



BL_Score = on_command('BL score', aliases={'BL查分', 'bl查分', 'bl40', 'BL40', 'b40', 'B40', 'bl 40', 'BL 40', 'b 40', 'B 40', 'BS查分', 'bs查分', 'bs40', 'BS40'}, priority=10)

@BL_Score.handle()
async def handle_BLScore(bot: Bot, event: Event):
    # 读取QQ号
    QQ_id = event.get_user_id()
    # 读取QQ号的BS_id
    player_id = await handle_BSid(QQ_id)
    if player_id == None :
        await BL_Score.finish('该账号未绑定SteamID')
    else:
        pass
    BL_datas = await api.BL_player_scores(player_id)
    if BL_datas == None:
        await BL_Score.finish('没注册BeatLeader或者网络出问题力QAQ')
    else:
        pass
    try:
        with open(f'{store.get_plugin_data_dir()}/{QQ_id}.json', 'r', encoding='utf-8') as data:
            old_data = json.load(data)
        old_data = old_data['BL_data']
    except:
        old_data = {}
        await BL_Score.send(MessageSegment.at(QQ_id) + f'\n第一次使用BeatLeader查分,请耐心等待~')
    bs_image = await draw.draw_image(Ranks_datas = BL_datas,old_data = old_data,cache_dir = store.get_plugin_cache_dir(),cache_file = store.get_plugin_cache_file('BS_cache.png'),data_dir = store.get_plugin_data_dir())
    if bs_image is None:
        await BL_Score.finish('绘图失败力')
    else:
        pass
    # 保存新数据
    storage.save_user_data(QQ_id,data_dir = store.get_plugin_data_dir(),datas = BL_datas)
    image_base64 = f'base64://{bs_image}'
    await BL_Score.send(MessageSegment.at(QQ_id) + f'\n[BeatLeader]' + MessageSegment.image(image_base64))
    try:
        # 删除缓存
        os.remove(store.get_plugin_cache_file('BS_cache.png'))
    except:
        pass
    return


SS_Score = on_command('SS score', aliases={'SS查分', 'ss查分', 'ss40', 'SS40', 'S40', 's40', 'SS 40', 'ss 40', 's 40', 'S 40', 'BS查分', 'bs查分', 'bs40', 'BS40'}, priority=10)

@SS_Score.handle()
# 复制粘贴
async def handle_SSScore(bot: Bot, event: Event):
    # 读取QQ号
    QQ_id = event.get_user_id()
    # 读取QQ号的BS_id
    player_id = await handle_BSid(QQ_id)
    if player_id == 114514 :
        await SS_Score.finish('该账号未绑定SteamID')
    else:
        pass
    try:
        with open(f'{store.get_plugin_data_dir()}/{QQ_id}.json', 'r', encoding='utf-8') as data:
            old_data = json.load(data)
        old_data = old_data['SS_data']
        id_data = old_data['songs']
    except:
        id_data = old_data = {}
    if old_data == {}:
        await SS_Score.send(MessageSegment.at(QQ_id) + f'\n第一次使用ScoreSaber查分,请耐心等待~')
    else:
        pass
    BS_data = await api.SS_player_scores(player_id,old_data = id_data)
    if BS_data == None:
        await SS_Score.finish('没注册ScoreSaber或者网络出问题力QAQ')
    bs_image = await draw.draw_image(Ranks_datas = BS_data,old_data = old_data,cache_dir = store.get_plugin_cache_dir(),cache_file = store.get_plugin_cache_file('SS_cache.png'),data_dir = store.get_plugin_data_dir(),SS = True)
    if bs_image is None:
        await SS_Score.finish('绘图失败力')
    else:
        pass

    image_base64 = f'base64://{bs_image}'
    await SS_Score.send(MessageSegment.at(QQ_id) + f'\n[ScoreSaber]' + MessageSegment.image(image_base64))
    storage.save_user_data(QQ_id,data_dir = store.get_plugin_data_dir(),datas = BS_data,SS = True)
    try:
        # 删除缓存
        os.remove(store.get_plugin_cache_file('SS_cache.png'))
    except:
        pass
    return

BS_Bind = on_command('BS bind', aliases={'节奏光剑绑定', 'BS绑定', 'bs绑定'}, priority=10)

@BS_Bind.handle()
async def handle_BS_Bind(bot: Bot, event: Event):
    QQ_id = event.get_user_id()
    message = str(event.get_message())
    data_dir = store.get_plugin_data_dir()
    save_status = storage.save_BSid(QQ_id, message,data_dir)
    if save_status == 19:
        return
    else:
        pass
    if save_status == 810:
        await BS_Bind.finish('写入数据出错辣!')
    else:
        pass
    player_id = await handle_BSid(QQ_id)
    BL_scores_data = await api.BL_player_scores(player_id,text = True)
    SS_scores_data = await api.SS_player_scores(player_id,text = True)
#    data_check = storage.save_user_data(QQ_id,data_dir,BL_scores_data,SS_scores_data)
    if BL_scores_data == 'BL_None' and SS_scores_data == 'SS_data':
        await BS_Bind.finish('SteamID绑定成功,但BeatLeader查询不到ID用户数据QAQ(单一账号不影响查分)')
    elif SS_scores_data == 'SS_None' and BL_scores_data == 'BL_data':
        await BS_Bind.finish('SteamID绑定成功,但ScoreSaber查询不到ID用户数据QAQ(单一账号不影响查分)')
    elif BL_scores_data == 'BL_None' and SS_scores_data == 'SS_None':
        await BS_Bind.finish('SteamID绑定成功,但ScoreSaber和BeatLeader查询不到ID用户数据QAQ')
    else:
        pass

    await BS_Bind.finish(save_status)

async def handle_BSid(QQ_id):
    with open(store.get_plugin_data_file('BSgroup.json'), 'r') as QQ_list:
        id_search = json.load(QQ_list)
    id = str(id_search[QQ_id])
    if id is None:
        return None
    else:
        # 不想改以前写的屎了
        id = id.replace("[", "").replace("]", "")
        id = id.replace("'", "").replace("'", "")
        return id
    
BS_Search = on_command('BS search', aliases={'节奏光剑查歌', 'BS查歌', 'bs查歌'}, priority=10)

@BS_Search.handle()
async def send_BS_Search(bot: Bot,event: GroupMessageEvent):
    message = str(event.get_message())
    if message.replace('BS查歌', '').replace('BS search', '').replace('节奏光剑查歌', '').replace('bs查歌', '').strip() == '':
        await BS_Search.finish('怎么啥都没写啊（｀＾´）')
    song_id = message.replace('BS查歌', '').replace('BS search', '').replace('节奏光剑查歌', '').replace('bs查歌', '').strip()
    song_information = await api.search_beatsaver(song_id)
    if song_information == None:
        await BS_Search.finish('无法获取歌曲信息,可能是id错误?')
    else:
        pass
    song_preview = song_information['versions'][0]['previewURL']
    song_cover = MessageSegment.image(song_information['versions'][0]['coverURL'])
    song_rank = []
    song_rank.append(song_information['ranked'])
    song_rank.append(song_information['blRanked'])
    # 判断这首歌是否是排位曲
    if song_rank[0] == True:
        ranking_ScoreSaber = 'ScoreSaber'
    else:
        ranking_ScoreSaber = 'None'
    # 如果这首歌是BeatLeader的排位曲,则获取其中的star
    if song_rank[1] == True:
        ranking_BeatLeader = 'BeatLeader'
        bl_song_star = []
        bl_song_diffs = []
        for version in song_information['versions']:
            for diffs in version['diffs']:
                bl_stars = diffs.get('blStars')
                if bl_stars != None:
                    bl_song_star.append(bl_stars)
                else:
                    pass
                bl_song_diffs.append(diffs['difficulty'])
    else:
        ranking_BeatLeader = 'None'
    rank_info = ''
    # 如果都不是排位曲,直接输出False
    rank_info = (f'{ranking_ScoreSaber} {ranking_BeatLeader}').replace('None', '')
    if rank_info == '':
        rank_info = 'False'
    else:
        pass
    # 如果只是BeatLeader排位曲,则删除前面多余的空格
    if ranking_BeatLeader == 'None':
        rank_info.strip()
    else:
        pass
    rank_star = ''
    #判断是否是BeatLeader的Rank曲
    if ranking_BeatLeader != 'None':
        i = 0
        for star in bl_song_star:
            rank_star += f'{bl_song_diffs[i]}:★{star}\n'
            i += 1
    else:
        rank_star = 'False'
    
    song_anydata =  MessageSegment.text(f"歌曲:{song_information['metadata']['songName']}\n曲师:{song_information['metadata']['songAuthorName']}\n谱面制作:{song_information['metadata']['levelAuthorName']}\nbpm:{song_information['metadata']['bpm']}\n排位曲:{rank_info}\n歌曲难度(BeatLeader)\n{rank_star}")
    await bot.send_group_msg(group_id = event.group_id, message = Message(song_cover + song_anydata))
    song_download = await retry.download_song_preview(url = song_preview,cache_path = store.get_plugin_cache_dir())
    if song_download == None:
        await BS_Search.finish('歌曲下载出错辣!')
    else:
        pass
    await BS_Search.finish(MessageSegment.record(song_download))



BS_Help = on_command('BS help', aliases={'节奏光剑帮助', 'BS帮助'}, priority=5)

@BS_Help.handle()
async def send_BS_Help():
    await BS_Help.finish('具体请查阅https://github.com/qwq12738qwq/nonebot-plugin-beatsaberscore的使用部分 (´・ω・`) ')

BS_calculate_acc = on_command('calculation', aliases={'谱面计算', '计算'}, priority=8)

@BS_calculate_acc.handle()
async def send_BS_calculation_acc(bot: Bot,event: GroupMessageEvent):
    message = str(event.get_message())
    if message == '':
        await BS_calculate_acc.finish('啥都没输入捏')
    else:
        pass
    msg_goal_acc = str(message.replace('calculation', '').replace('谱面计算', '').replace('计算', '').strip())
    # 提取准度(匹配数字+小数点+%号)
    msg_goal_acc = re.search(r'\d+\.\d+%', msg_goal_acc)
    if msg_goal_acc == None:
        await BS_calculate_acc.finish('是不是少了准度没输入捏（＞д＜）')
    goal_acc = msg_goal_acc.group()
    # 提取歌曲ID
    song_id = message.replace(f'{goal_acc}', '').replace(f'Easy', '').replace(f'Normal', '').replace(f'Hard', '').replace(f'Expert', '').replace(f'ExpertPlus', '').replace('calculation', '').replace('谱面计算', '').replace('计算', '').strip()
    # 提取歌曲难度
    song_difficulty = (message.replace(f'{goal_acc}', '').replace(f'{song_id}', '').replace('calculation', '').replace('谱面计算', '').replace('计算', '').strip())
    song_information = await api.search_beatsaver(song_id)
    if song_information == None:
        await BS_calculate_acc.finish('网络出问题辣,请重试一次吧（｀＾´）')
    else:
        pass
    song_cover = MessageSegment.image(song_information['versions'][0]['coverURL'])
    song_diffs = []
    song_maxnotes = []
    diffs_to_maxscore = {}
    # 提取难度
    for version in song_information['versions']:
        for diffs in version['diffs']:
            song_diffs.append(diffs['difficulty'])
        for maxscore in version['diffs']:
            song_maxnotes.append(maxscore['notes'])
    # 去掉%用于计算
    i = 0
    for diffs in song_diffs:
        diffs_to_maxscore[f'{diffs}'] = song_maxnotes[i]
        i += 1

    total_notes =  diffs_to_maxscore[f'{song_difficulty}']
    goal_acc = (message.replace(f'{song_id}', '').replace('%', '').replace(f'Easy', '').replace(f'Normal', '').replace(f'Hard', '').replace(f'Expert', '').replace(f'ExpertPlus', '').replace('calculation', '').replace('谱面计算', '').replace('计算', '').strip())
    calculation_acc = calculation.calculate_acc_note(goal_acc = float(goal_acc), total_notes = int(total_notes))
    song_info = f"歌曲:{song_information['metadata']['songName']}\n歌曲难度:{song_difficulty}\n总Note数:{total_notes}\n达到{goal_acc}%在平均分110不连续miss情况下最大miss次数:{(calculation_acc['double_max_miss'])}\n达到{goal_acc}%需要获得的分数:{calculation_acc['goal_score']}"
    await BS_calculate_acc.finish(group_id = event.group_id, message = Message(song_cover + song_info))
