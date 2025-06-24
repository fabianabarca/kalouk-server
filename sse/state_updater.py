import asyncio
import random
import redis.asyncio as redis_aio
from scipy.stats import expon


async def state_updater():
    async with redis_aio.from_url("redis://localhost") as redis:
        state = 0
        await redis.publish("state_updates", str(state))
        while True:
            delay, next_state = update_state(state)
            print(f"Current state: {state}, Next state: {next_state}, Delay: {delay}")
            await asyncio.sleep(delay)
            state = next_state
            await redis.publish("state_updates", str(state))


def update_state(state):
    lam = 15.001 / 60
    nu = 15.002 / 60
    if state == 0:
        delay = expon.rvs(scale=1 / lam)
        next_state = 1
    else:
        delay = expon.rvs(scale=1 / (lam + nu))
        p = lam / (lam + nu)
        q = 1 - p
        step = random.choices([1, -1], weights=[p, q], k=1)[0]
        print(f"Step chosen: {step} (p={p}, q={q})")
        next_state = state + step
    return delay, next_state
