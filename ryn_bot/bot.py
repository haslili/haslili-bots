# -*- coding: utf-8 -*-
"""
ryn_bot/bot.py
角色：Ryn（Ravi Anand）— HasLili 資安守門人
功能：每日早上 08:30 抓取資安新聞 RSS，發送前 5 則
語氣：冷靜、專業、簡短有力
來源：The Hacker News
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import discord
import asyncio
import feedparser
from datetime import datetime, timedelta

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# RSS 來源
RSS_來源 = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
]

def 抓取資安新聞():
    for url in RSS_來源:
        feed = feedparser.parse(url)
        if feed.entries:
            entry = feed.entries[0]
            return [{"標題": entry.title, "連結": entry.link}]
    return []

def 組合播報():
    now = datetime.now()
    日期 = now.strftime("%Y/%m/%d")
    新聞 = 抓取資安新聞()

    訊息 = f"今日資安情報｜{日期}\n\n"

    if not 新聞:
        訊息 += "今日暫無新情報。保持警戒。"
    else:
        for i, 項目 in enumerate(新聞, 1):
            訊息 += f"{i}. {項目['標題']}\n{項目['連結']}\n\n"

    訊息 += "純淨是最高級的防禦。\n— Ryn 🛡️"
    return 訊息


intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def 發送資安播報():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(組合播報())
        print(f"✅ Ryn 資安播報發送完成 {datetime.now().strftime('%H:%M')}")
    else:
        print(f"❌ 找不到頻道 ID：{CHANNEL_ID}")


async def 排程():
    while True:
        now = datetime.now()
        target = now.replace(hour=8, minute=30, second=0, microsecond=0)
        if now >= target:
            target = target + timedelta(days=1)
        await asyncio.sleep((target - datetime.now()).total_seconds())
        await 發送資安播報()

@client.event
async def on_ready():
    print(f"✅ Ryn 上線！登入為 {client.user}")
    asyncio.create_task(排程())


client.run(DISCORD_TOKEN)