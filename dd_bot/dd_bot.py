# -*- coding: utf-8 -*-
import discord
import requests
import asyncio
from datetime import datetime

# ══ 填入金鑰 ══
DISCORD_TOKEN = ""  # 填入 Token（請勿直接寫在此處，使用 config.py）
CHANNEL_ID = 1490035117870288977
# ══════════════

def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,solana,binancecoin,sonic-3",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        def fmt(coin_id, name, symbol):
            coin = data.get(coin_id, {})
            price = coin.get("usd", 0)
            change = coin.get("usd_24h_change", 0)
            arrow = "▲" if change >= 0 else "▼"
            return f"{symbol} {name}：${price:,.2f} {arrow} {change:+.2f}%"

        lines = [
            fmt("bitcoin", "BTC", "🟡"),
            fmt("ethereum", "ETH", "🔵"),
            fmt("solana", "SOL", "🟣"),
            fmt("binancecoin", "BNB", "🟠"),
            fmt("sonic-3", "S (Sonic)", "🌊"),
        ]
        return "\n".join(lines)
    except Exception as e:
        return f"❌ 幣價抓取失敗：{e}"

def get_fear_greed():
    try:
        response = requests.get(
            "https://api.alternative.me/fng/", timeout=10)
        data = response.json()
        value = data["data"][0]["value"]
        label = data["data"][0]["value_classification"]
        return f"{value} / 100 — {label}"
    except:
        return "無法取得"

def build_report():
    now = datetime.now().strftime("%Y/%m/%d %H:%M")
    prices = get_crypto_prices()
    fg = get_fear_greed()

    report = f"""🌙 **HasLili DD 每日情報** ｜ {now}

📊 **主要幣價**
{prices}

😱 **市場恐懼貪婪指數**
{fg}

---
*「我不是衝很快，我只是比你早一點聞到不對。」*
— DD，HasLili 獵手"""
    return report

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ DD 上線！登入為 {client.user}")
    await send_daily_report()

async def send_daily_report():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    while True:
        report = build_report()
        if channel:
            await channel.send(report)
            print(f"✅ 報告已發送")
        # 每24小時發一次
        await asyncio.sleep(86400)

client.run(DISCORD_TOKEN)
