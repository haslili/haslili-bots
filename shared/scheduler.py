# -*- coding: utf-8 -*-
"""
shared/scheduler.py
HasLili Discord Bot 排程模組
支援每日定時觸發（指定 HH:MM）
"""
import asyncio
from datetime import datetime, timedelta


async def wait_until(hour: int, minute: int = 0):
    """等待到今天（或明天）的指定時間"""
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    wait_seconds = (target - now).total_seconds()
    print(f"⏰ 等待到 {target.strftime('%Y/%m/%d %H:%M')}，約 {wait_seconds/3600:.1f} 小時後觸發")
    await asyncio.sleep(wait_seconds)


async def daily_task(hour: int, minute: int, task_func):
    """
    每天在指定時間執行 task_func
    用法：asyncio.create_task(daily_task(8, 0, my_func))
    """
    while True:
        await wait_until(hour, minute)
        await task_func()


async def interval_task(seconds: int, task_func):
    """
    每隔 N 秒執行一次 task_func
    用法：asyncio.create_task(interval_task(86400, my_func))
    """
    while True:
        await task_func()
        await asyncio.sleep(seconds)
