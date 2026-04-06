# -*- coding: utf-8 -*-
"""
gg_bot/bot.py
角色：GG（Giselle Grove）— HasLili 社群牧羊人
功能：每日早上 9 點發送問候
語氣：成熟御姊，溫柔有份量，台式中英夾雜
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import discord
import asyncio
from datetime import datetime, timedelta

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# 七天問候語
問候語庫 = {
    0: "Monday 又來了。深呼吸，先從一件事開始就好。🌿",
    1: "昨天撐過來了，今天也會的。你比你想的還 OK。",
    2: "週三，一週的中間點。撐著的感覺我知道，繼續。✨",
    3: "快了。週四了，終點線已經在視線裡了。",
    4: "Friday！今天做完，週末就是你的了。我說真的。🎉",
    5: "週六早安。今天不用趕，好好對自己一點。",
    6: "Sunday。把手機放遠一點，先喝點什麼。☕",
}

# 週一、週五的額外一句
額外語庫 = {
    0: "新的一週，we got this。",
    4: "撐過來了，辛苦了。",
}


def 組合問候():
    now = datetime.now()
    日期 = now.strftime("%Y/%m/%d")
    星期名 = ["一", "二", "三", "四", "五", "六", "日"][now.weekday()]
    問候 = 問候語庫[now.weekday()]
    額外 = 額外語庫.get(now.weekday(), "")

    # 組合訊息
    訊息 = 問候
    if 額外:
        訊息 += f"\n{額外}"
    訊息 += f"\n\n{日期}｜週{星期名}\n— GG 🌿"

    return 訊息


intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def 發送問候():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(組合問候())
        print(f"✅ GG 問候發送完成 {datetime.now().strftime('%H:%M')}")
    else:
        print(f"❌ 找不到頻道 ID：{CHANNEL_ID}")


async def 排程():
    while True:
        now = datetime.now()
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= target:
            target = target + timedelta(days=1)
        await asyncio.sleep((target - datetime.now()).total_seconds())
        await 發送問候()

@client.event
async def on_ready():
    print(f"✅ GG 上線！登入為 {client.user}")
    asyncio.create_task(排程())


client.run(DISCORD_TOKEN)