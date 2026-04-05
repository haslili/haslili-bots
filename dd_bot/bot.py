# -*- coding: utf-8 -*-
"""
dd_bot/bot.py
角色：DD（Dahlia Drift）— HasLili 幣價獵手
功能：每日 20:00 播報幣價 + 恐懼貪婪指數
語氣：活潑、直接、有獵性，偶爾嘴一下市場
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import discord
import requests
import asyncio
from datetime import datetime, timedelta

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# DD 的每日開場白，隨星期幾輪替
開場白庫 = {
    0: "週一盤，最難讀的一天。不過難不過我就是了。",
    1: "週二，市場還在找方向。我已經聞到了。",
    2: "週三，一週最容易假突破的時候。小心。",
    3: "週四，有時候這天才是真正要動的。眼睛放亮。",
    4: "週五，收盤前的情緒最亂。不要被帶走。",
    5: "週六。不是所有人都在休息，我沒有。",
    6: "週日。下週的事，現在就開始想了。",
}

# 恐懼貪婪指數評語
def DD評語(value: int) -> str:
    if value <= 15:
        return "這是極度恐慌。歷史上這種時候⋯⋯你懂的。👀"
    elif value <= 30:
        return "市場在怕。DD 開始聞味道了。"
    elif value <= 45:
        return "偏悲觀，但還沒崩。繼續觀察。"
    elif value <= 55:
        return "中性。大家都在等，包括我。"
    elif value <= 70:
        return "有點貪了。這種時候要反問自己。"
    elif value <= 85:
        return "貪婪升溫中。DD 建議你深呼吸。🚨"
    else:
        return "極度貪婪！⚠️ 這種時候 DD 會開始找出口。"

def 取得幣價():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,solana,binancecoin,sonic-3",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        def 格式化(coin_id, 名稱, 符號):
            coin = data.get(coin_id, {})
            price = coin.get("usd", 0)
            change = coin.get("usd_24h_change", 0)
            arrow = "▲" if change >= 0 else "▼"
            # 漲跌超過5%加備註
            備註 = ""
            if change >= 5:
                備註 = " 🔥"
            elif change <= -5:
                備註 = " 🩸"
            return f"{符號} {名稱}　${price:,.2f}　{arrow} {change:+.2f}%{備註}"

        幣種清單 = [
            ("bitcoin",     "BTC",       "🟡"),
            ("ethereum",    "ETH",       "🔵"),
            ("solana",      "SOL",       "🟣"),
            ("binancecoin", "BNB",       "🟠"),
            ("sonic-3",     "S (Sonic)", "🌊"),
        ]
        return "\n".join(格式化(cid, name, sym) for cid, name, sym in 幣種清單)
    except Exception as e:
        return f"❌ 幣價抓取失敗：{e}"


def 取得恐懼貪婪():
    try:
        res = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = res.json()
        value = int(data["data"][0]["value"])
        label = data["data"][0]["value_classification"]
        評語 = DD評語(value)
        return f"{value} / 100 — {label}\n{評語}"
    except:
        return "今天抓不到，市場情緒自己感受一下。"


def 組合報告():
    now = datetime.now()
    時間 = now.strftime("%Y/%m/%d %H:%M")
    開場 = 開場白庫[now.weekday()]
    幣價 = 取得幣價()
    fg = 取得恐懼貪婪()

    return f"""DD 來了。｜ {時間}

{開場}

📊 幣價快照
{幣價}

😱 市場情緒
{fg}

「我不是衝很快，我只是比你早一點聞到不對。」
— DD 🔫"""


intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def 發送報告():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(組合報告())
        print(f"✅ DD 報告發送完成 {datetime.now().strftime('%H:%M')}")
    else:
        print(f"❌ 找不到頻道 ID：{CHANNEL_ID}")


async def 排程():
    while True:
        now = datetime.now()
        target = now.replace(hour=20, minute=0, second=0, microsecond=0)
        if now >= target:
            target = target + timedelta(days=1)
        await asyncio.sleep((target - datetime.now()).total_seconds())
        await 發送報告()

@client.event
async def on_ready():
    print(f"✅ DD 上線！登入為 {client.user}")
    await 發送報告()  # 上線立即發一次
    asyncio.create_task(排程())


client.run(DISCORD_TOKEN)