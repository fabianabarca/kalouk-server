from channels.generic.http import AsyncHttpConsumer
import asyncio
import redis.asyncio as redis_aio
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class StateSSEConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        logger.info("SSE connection established")
        await self.send_headers(
            headers=[
                (b"Content-Type", b"text/event-stream"),
                (b"Access-Control-Allow-Origin", b"*"),
            ]
        )

        redis = await redis_aio.from_url("redis://localhost")
        pubsub = redis.pubsub()
        await pubsub.subscribe("state_updates")
        logger.info("Subscribed to state_updates channel")

        try:
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=0.01
                )
                if message and message["type"] == "message":
                    data = message["data"].decode()
                    logger.info(f"Received message: {data}")
                    timestamp = int(datetime.now().timestamp() * 1000)
                    json_payload = json.dumps({"state": data, "timestamp": timestamp})
                    payload = f"data: {json_payload}\n\n"
                    await self.send_body(payload.encode(), more_body=True)
                    logger.info(f"Sent SSE message: {payload.strip()}")
                else:
                    await self.send_body(b": heartbeat\n\n", more_body=True)
        except asyncio.CancelledError:
            logger.info("SSE connection cancelled")
            await pubsub.unsubscribe("state_updates")
            await pubsub.close()
        except Exception as e:
            logger.error(f"SSE error: {e}")
            await pubsub.unsubscribe("state_updates")
            await pubsub.close()
