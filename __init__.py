import os
import base64
from nonebot import on_command
from pathlib import Path
from playwright.async_api import async_playwright
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

url = "https://beatleader.xyz/u/76561198949185975"

BS_Score = on_command("BS查分", aliases={"节奏光剑查分"}, priority=10)

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
    await BS_Score.send(MessageSegment.image(image_base64))
