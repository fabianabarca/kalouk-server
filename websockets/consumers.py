import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)


class TestConsumer(AsyncWebsocketConsumer):
    """This simple test responds to a WebSocket connection with a 'Hello' message."""

    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        # Send a message to the WebSocket
        await self.send(text_data=json.dumps({"message": "Hola desde el servidor"}))

    async def disconnect(self, code):
        # Handle disconnection if needed
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # Handle incoming messages if needed
        pass


class SlidevSyncConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_id = None
        self.group_name = None
        self.device_uid = None

    async def connect(self):
        """Accept WebSocket connection"""
        await self.accept()
        logger.info(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, code):
        """Handle WebSocket disconnection"""
        if self.group_name and self.channel_layer is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f"Client {self.device_uid} left group {self.group_id}")

    async def receive(self, text_data=None, bytes_data=None):
        """Handle incoming WebSocket messages"""
        try:
            if text_data is None:
                logger.error("No text_data received")
                return
            data = json.loads(text_data)
            message_type = data.get("type")

            if message_type == "connect":
                await self.handle_connect(data)
            elif message_type == "patch":
                await self.handle_patch(data)
            else:
                logger.warning(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def handle_connect(self, data):
        """Handle client connection to a group"""
        self.group_id = data.get("id")
        self.device_uid = data.get("uid")
        states = data.get("states", {})

        if not self.group_id or not self.device_uid:
            logger.error("Missing group_id or device_uid in connect message")
            return

        # Create group name for channels
        self.group_name = f"slidev_group_{self.group_id}"

        # Join the group
        if self.channel_layer is not None:
            await self.channel_layer.group_add(self.group_name, self.channel_name)

        logger.info(f"Client {self.device_uid} joined group {self.group_id}")

        # Store/update group states if provided
        if states:
            await self.update_group_states(self.group_id, states)

            # Broadcast initial states to other clients in the group
            if self.channel_layer is not None:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "sync_message",
                        "states": states,
                        "message_type": "replace",  # or 'patch'
                        "sender_uid": self.device_uid,
                    },
                )

    async def handle_patch(self, data):
        """Handle state patch updates"""
        group_id = data.get("id")
        states = data.get("states", {})
        device_uid = data.get("uid")

        if not group_id or not device_uid:
            logger.error("Missing group_id or device_uid in patch message")
            return

        # Update group states
        await self.update_group_states(group_id, states)

        # Broadcast to group (excluding sender)
        patch_message = {
            "type": "sync_message",
            "states": states,
            "message_type": "patch",
            "sender_uid": device_uid,
        }
        if self.channel_layer is not None:
            await self.channel_layer.group_send(self.group_name, patch_message)
        logger.info(f"Client {device_uid} sent patch to group {group_id}")

    async def sync_message(self, event):
        """Send sync message to WebSocket client"""
        states = event["states"]
        message_type = event["message_type"]
        sender_uid = event["sender_uid"]

        # Don't send message back to sender
        if sender_uid == self.device_uid:
            return

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"states": states, "type": message_type, "uid": sender_uid}
            )
        )

    @database_sync_to_async
    def update_group_states(self, group_id, states):
        """Update group states in database (optional persistence)"""
        # You can implement state persistence here if needed
        # For now, we rely on channel layer for in-memory state
        pass


class DeckSliderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.deck_id = self.scope["url_route"]["kwargs"]["deck_id"]
        self.deck_group_name = f"deck_{self.deck_id}"
        print(self.deck_group_name)
        print(self.channel_name)
        print(self.deck_id)

        # Join demo group
        if self.channel_layer is not None:
            await self.channel_layer.group_add(self.deck_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(
                self.deck_group_name, self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            indexh = text_data_json["indexh"]
            indexv = text_data_json["indexv"]

            # Send message to demo group
            if self.channel_layer is not None:
                await self.channel_layer.group_send(
                    self.deck_group_name,
                    {
                        "type": "slide_changed",
                        "message": {"indexh": indexh, "indexv": indexv},
                    },
                )

    # Receive message from room group
    async def slide_changed(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
