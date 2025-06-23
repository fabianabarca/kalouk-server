# app/state_updater.py
import asyncio
import random
import redis.asyncio as redis_aio


async def state_updater():
    redis = await redis_aio.from_url("redis://localhost")
    while True:
        await asyncio.sleep(random.uniform(1, 5))
        state = random.randint(1, 100)
        await redis.publish("state_updates", str(state))
