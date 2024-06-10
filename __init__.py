import re
import os
import json
import base64
from collections import defaultdict
from nonebot import on_command
from pathlib import Path
from playwright.async_api import async_playwright
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="BS查分",
    description="从beatleader获取个人信息并查看PP",
    type="application",
    usage="BSScore",
    homepage="https://github.com/qwq12738qwq/Nonebot_BeatSaber_BLScore",
    supported_adapters={"nonebot.adapters.onebot.v11"},
)

# 双引号里面的url自己加上去捏,登入自己的beatleader账号,在个人主页上的网址复制到引号里面就可以用了
URL = "https://beatleader.xyz/u/"

BS_Score = on_command("BS查分", aliases={"节奏光剑查分"}, priority=10)
BS_Bind = on_command("BS绑定", aliases={"节奏光剑绑定"}, priority=10)

async def BS_Score_Search(url):

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        # 等待网页加载
        await page.wait_for_load_state('networkidle')
        # 截取网页并保存
        await page.screenshot(path="data/BSScore.jpg", full_page=True)
        # 关闭浏览器
        await browser.close()

@BS_Score.handle()

async def handle_BSScore(bot: Bot, event: Event):
    # 读取QQ号
    QQ_id = event.get_user_id()
    # 读取QQ号的BS_id
    with open('data/BSgroup.json', 'r') as json_file:
        data = json_file.read()
    id_search = json.loads(data)
    id = str(id_search[QQ_id])
    # 去除id中的中括号
    id = id.replace("[", "").replace("]", "")
    # 去除id中的''
    id = id.replace("'", "").replace("'", "")
    if not id is None:
        url = URL + id
        # 开始截图函数
        await BS_Score_Search(url)
        # 设置存储目录(自己找自己的目录罢)
        save_path = Path("/root/Bot/QQbot/data/") 
        img_name = "BSScore.jpg"
        img = save_path / img_name
        # base64编码(编码才能发送图片,坑我好久QAQ)
        with open(img, "rb") as image_file:
             encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        image_base64 = f"base64://{encoded_string}"
        await BS_Score.finish(MessageSegment.image(image_base64))
    else:
        msg = "该QQ账号未绑定"
        await BS_Score.finish(msg)

@BS_Bind.handle()

async def handle_BS_Bind(bot: Bot, event: Event):
    QQ_id = event.get_user_id()
    message = str(event.get_message())
    id_list = re.findall(r'\d+', message)
    # 将列表的数字提取出来
    BS_id = id_list[0]
    # 检测是否有json文件
    try:
        with open('data/BSgroup.json', 'r') as f:
            Groud_data = json.load(f)
    except FileNotFoundError:
        Groud_data = {}
    # 创建字典
    Groud_data = {
        QQ_id: BS_id
    }
    # 初始化列表防止报KeyError错误
    Groud_data = defaultdict(list)
    Groud_data[QQ_id].append(BS_id)
    # 写入数据到json
    with open('data/BSgroup.json', 'w') as f:
        json.dump(Groud_data, f, sort_keys=True, indent=4)
    #尝试读取文件看是否写入
    try:
        with open('data/BSgroup.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if data == {}:
        test = "数据存储失败"
        await BS_Bind.finish(test)
    else:
        pass
    msg = "QQ号:" + QQ_id + "已绑定beatleaderID:" + BS_id
    await BS_Bind.finish(msg)
