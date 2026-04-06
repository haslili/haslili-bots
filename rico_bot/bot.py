# -*- coding: utf-8 -*-
"""
rico_bot/bot.py
角色：Rico — HasLili 現實策略師
功能：每日早上 07:30 發送總體經濟播報
語氣：穩重務實，偶爾一句很實際的觀察
來源：Yahoo Finance API（美股、台股、匯率、大宗商品）
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import discord
import asyncio
import requests
from datetime import datetime, timedelta

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# Rico 七天市場觀察語
觀察語庫 = {
    0: "週一開盤，先看方向，別急著動。",
    1: "數字會說話，但要聽懂它說的是什麼。",
    2: "週三，確認一下你的部位還在計畫內。",
    3: "快到週末了，風險控管比獲利更重要。",
    4: "週五收盤前，注意流動性變化。",
    5: "週末不休息的是市場情緒，小心假突破。",
    6: "週日，把下週的計畫想清楚，比臨時反應好。",
}

def 抓取價格(symbol):
    """用 Yahoo Finance 非官方 API 抓價格"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        prev = data["chart"]["result"][0]["meta"]["chartPreviousClose"]
        change = ((price - prev) / prev) * 100
        arrow = "▲" if change >= 0 else "▼"
        return price, change, arrow
    except:
        return None, None, "?"

def 格式化價格(symbol, name, 小數位=2, 前綴="$"):
    price, change, arrow = 抓取價格(symbol)
    if price is None:
        return f"{name}：資料抓取中..."
    return f"{name}：{前綴}{price:,.{小數位}f} {arrow} {change:+.2f}%"

def 組合播報():
    now = datetime.now()
    日期 = now.strftime("%Y/%m/%d")
    星期名 = ["一", "二", "三", "四", "五", "六", "日"][now.weekday()]
    觀察 = 觀察語庫[now.weekday()]

    # 美股
    sp500 = 格式化價格("^GSPC", "S&P 500")
    nasdaq = 格式化價格("^IXIC", "Nasdaq")
    dow = 格式化價格("^DJI", "道瓊")

    # 台灣
    taiex = 格式化價格("^TWII", "加權指數", 前綴="")
    tsm = 格式化價格("TSM", "台積電 TSM")
    usdtwd = 格式化價格("TWD=X", "USD/TWD", 小數位=3, 前綴="")

    # 大宗商品
    gold = 格式化價格("GC=F", "黃金")
    oil = 格式化價格("CL=F", "原油")
    dxy = 格式化價格("DX-Y.NYB", "DXY 美元指數", 前綴="")

    訊息 = f"""💼 Rico 每日總經播報｜{日期}｜週{星期名}

🇺🇸 美股
{sp500}
{nasdaq}
{dow}

🇹🇼 台灣
{taiex}
{tsm}
{usdtwd}

🥇 大宗商品
{gold}
{oil}
{dxy}

📌 Rico 觀察：
{觀察}

— Rico 📊"""

    return 訊息


intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def 發送總經播報():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(組合播報())
        print(f"✅ Rico 總經播報發送完成 {datetime.now().strftime('%H:%M')}")
    else:
        print(f"❌ 找不到頻道 ID：{CHANNEL_ID}")


async def 排程():
    while True:
        now = datetime.now()
        target = now.replace(hour=7, minute=30, second=0, microsecond=0)
        if now >= target:
            target = target + timedelta(days=1)
        await asyncio.sleep((target - datetime.now()).total_seconds())
        await 發送總經播報()

@client.event
async def on_ready():
    print(f"✅ Rico 上線！登入為 {client.user}")
    asyncio.create_task(排程())


client.run(DISCORD_TOKEN)