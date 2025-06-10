import json

from channels.generic.websocket import AsyncWebsocketConsumer


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
