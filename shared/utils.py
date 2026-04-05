# -*- coding: utf-8 -*-
"""
shared/utils.py
HasLili Discord Bot 共用工具函數
"""
import discord


async def send_message(client: discord.Client, channel_id: int, content: str):
    """發送訊息到指定頻道"""
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(content)
        return True
    else:
        print(f"❌ 找不到頻道 ID：{channel_id}")
        return False


async def send_embed(client: discord.Client, channel_id: int, embed: discord.Embed):
    """發送 Embed 訊息到指定頻道"""
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(embed=embed)
        return True
    else:
        print(f"❌ 找不到頻道 ID：{channel_id}")
        return False
