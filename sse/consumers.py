from channels.generic.http import AsyncHttpConsumer
import asyncio
import redis.asyncio as redis_aio


class StateSSEConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        await self.send_headers(headers=[(b"Content-Type", b"text/event-stream")])

        redis = await redis_aio.from_url("redis://localhost")
        pubsub = redis.pubsub()
        await pubsub.subscribe("state_updates")

        try:
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message and message["type"] == "message":
                    data = message["data"].decode()
                    payload = f"data: {data}\n\n"
                    await self.send_body(payload.encode(), more_body=True)
                else:
                    await self.send_body(b": heartbeat\n\n", more_body=True)
        except asyncio.CancelledError:
            await pubsub.unsubscribe("state_updates")
            await pubsub.close()
