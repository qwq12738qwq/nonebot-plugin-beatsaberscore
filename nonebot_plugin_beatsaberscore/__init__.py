import os
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot import require
require('nonebot_plugin_localstore')
import nonebot_plugin_localstore as store
from .config import Config
from . import api, draw, storage, retry

__version__ = "0.9.6"
__plugin_meta__ = PluginMetadata(
    name="Beat Saber查分器",
    description="Nonebot2的节奏光剑查分插件,支持BeatLeader&ScoreSaber查分",
    type="application",
    config=Config,
    usage="BL score, SS score, BS bind, BS help",
    homepage="https://github.com/qwq12738qwq/nonebot-plugin-beatsaberscore",
    supported_adapters={"~onebot.v11"},
)



BL_Score = on_command('BL score', aliases={'BL查分'}, priority=10)

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
    scores_total = await api.BL_player_scores(player_id)
    player_total = await api.BL_handle_player(player_id)
    if scores_total == None or player_total == None:
        await BL_Score.finish('没注册beatleader或者网络真出问题力QAQ')
    elif scores_total == 1919810:
        await BL_Score.finish('json数据损坏或无法打开,再重试一下罢')
        
    with open(store.get_plugin_data_file(f'{QQ_id}.json'), 'r') as json_file:
        old_data = json.loads(json_file.read())
    bs_image = await draw.draw_image(scores_total,player_total,old_data,cache_dir = store.get_plugin_cache_dir(),cache_file = store.get_plugin_cache_file('BS_cache.png'))
    if bs_image is None:
        await BL_Score.finish('绘图失败力')
    else:
        pass
    # 保存新数据
#    storage.save_user_data(QQ_id,data_dir = store.get_plugin_data_dir(),scores_data = scores_total)

    image_base64 = f'base64://{bs_image}'
    try:
        await BL_Score.finish(MessageSegment.image(image_base64))
    finally:
        # 删除缓存
        os.remove(store.get_plugin_cache_file('BS_cache.png'))

SS_Score = on_command('SS score', aliases={'SS查分'}, priority=10)

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
    scores_total = await api.SS_player_scores(player_id)
    player_total = await api.SS_handle_player(player_id)
    if scores_total == None or player_total == None:
        await SS_Score.finish('没注册beatleader或者网络真出问题力QAQ')
    elif scores_total == 1919810:
        await SS_Score.finish('json数据损坏或无法打开,再重试一下罢')
    # 补全缺少的top_pp
    player_total['top_pp'] = scores_total['song_pp'][0]
        
    with open(store.get_plugin_data_file(f'{QQ_id}.json'), 'r') as json_file:
        old_data = json.loads(json_file.read())
    bs_image = await draw.draw_image(scores_total,player_total,old_data,cache_dir = store.get_plugin_cache_dir(),cache_file = store.get_plugin_cache_file('BS_cache.png'),SS = True)
    if bs_image is None:
        await SS_Score.finish('绘图失败力')
    else:
        pass
    # 保存新数据
#    storage.save_user_data(QQ_id,data_dir = store.get_plugin_data_dir(),scores_data = scores_total)

    image_base64 = f'base64://{bs_image}'
    try:
        await SS_Score.finish(MessageSegment.image(image_base64))
    finally:
        # 删除缓存
        os.remove(store.get_plugin_cache_file('BS_cache.png'))

BS_Bind = on_command('BS bind', aliases={'节奏光剑绑定', 'BS绑定'}, priority=10)

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
    BL_scores_data = await api.BL_player_scores(player_id)
    SS_scores_data = await api.SS_player_scores(player_id)
    data_check = storage.save_user_data(QQ_id,data_dir,BL_scores_data,SS_scores_data)
    if data_check == 'BL_None':
        await BS_Bind.finish('SteamID绑定成功,但BeatLeader查询不到ID用户数据QAQ')
    elif data_check == 'SS_None':
        await BS_Bind.finish('SteamID绑定成功,但ScoreSaber查询不到ID用户数据QAQ')
    elif data_check == None:
        await BS_Bind.finish('SteamID绑定成功,但ScoreSaber和BeatLeader查询不到ID用户数据QAQ')
    else:
        pass

    await BS_Bind.finish(save_status)

async def handle_BSid(QQ_id):
    with open(store.get_plugin_data_file('BSgroup.json'), 'r') as json_file:
        QQ_data = json_file.read()
    id_search = json.loads(QQ_data)
    id = str(id_search[QQ_id])
    if id is None:
        return None
    else:
        # 不想改以前写的屎了
        id = id.replace("[", "").replace("]", "")
        id = id.replace("'", "").replace("'", "")
        return id
    
BS_Search = on_command('BS search', aliases={'节奏光剑查歌', 'BS查歌'}, priority=10)

@BS_Search.handle()
async def send_BS_Search(bot: Bot,event: GroupMessageEvent):
    message = str(event.get_message())
    song_id = message.replace('BS查歌', '').replace('BS search', '').replace('节奏光剑查歌', '').strip()
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
    await BS_Help.send('具体请查阅https://github.com/qwq12738qwq/nonebot-plugin-beatsaberscore的使用部分 (´・ω・`) ')