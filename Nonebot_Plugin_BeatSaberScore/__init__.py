import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.plugin import PluginMetadata
from . import api
from . import draw
from . import save

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-beatsaberscore",
    description="Nonebot2的Beat Saber查分器",
    type="application",
    usage="BS score, BS bind, BS help",
    homepage="https://github.com/qwq12738qwq/nonebot-plugin-beatsaberscore",
    supported_adapters={"~onebot.v11"},
)


BS_Score = on_command('BS score', aliases={'节奏光剑查分', 'BS查分'}, priority=10)
BS_Bind = on_command('BS bind', aliases={'节奏光剑绑定', 'BS绑定'}, priority=10)
BS_Help = on_command('BS help', aliases={'节奏光剑帮助', 'BS帮助'}, priority=5)

@BS_Score.handle()
async def handle_BSScore(bot: Bot, event: Event):
    # 读取QQ号
    QQ_id = event.get_user_id()
    # 读取QQ号的BS_id
    player_id = await handle_BSid(QQ_id)
    if player_id == 114514 :
        await BS_Score.finish('该账号未绑定beatleader的ID')

    scores_total = await api.player_scores(player_id)
    player_total = await api.handle_player(player_id)
    if scores_total == 114514 or player_total == 114514:
        await BS_Score.finish('没注册beatleader或者网络真出问题力QAQ')
    elif scores_total == 1919810:
        await BS_Score.finish('json数据损坏或无法打开,再重试一下罢')
        
    bs_image = await draw.draw_image(scores_total,player_total)
    if bs_image is None:
        await BS_Score.finish('绘图失败力')
    else:
        pass
        
    image_base64 = f"base64://{bs_image}"
    
    await BS_Score.finish(MessageSegment.image(image_base64))

@BS_Bind.handle()
async def handle_BS_Bind(bot: Bot, event: Event):
    QQ_id = event.get_user_id()
    message = str(event.get_message())
    save_status = save.save_BSid(QQ_id, message)
    if save_status == 19:
        return
    if save_status == 810:
        await BS_Bind.finish('写入数据出错辣!')
    await BS_Bind.finish(save_status)

async def handle_BSid(QQ_id):
    with open('data/BSgroup.json', 'r') as json_file:
        data = json_file.read()
    id_search = json.loads(data)
    id = str(id_search[QQ_id])
    if id is None:
        return 114514
    else:
        # 去除id中的中括号
        id = id.replace("[", "").replace("]", "")
        # 去除id中的''
        id = id.replace("'", "").replace("'", "")
        return id

@BS_Help.handle()
async def send_BS_Help():
    await BS_Help.send('具体请查阅https://github.com/qwq12738qwq/nonebot-plugin-beatsaberscore的使用部分 (´・ω・`) ')