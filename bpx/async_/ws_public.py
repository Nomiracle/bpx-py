import asyncio
import websockets
import json
from typing import Callable, Optional, Dict, Any
from bpx.base.base_ws_public import BaseWsPublic


class WsPublic(BaseWsPublic):
    """
    Asynchronous WebSocket client for public streams
    """

    def __init__(self, on_message: Optional[Callable] = None, on_error: Optional[Callable] = None,
                 on_close: Optional[Callable] = None, on_open: Optional[Callable] = None):
        """
        Initialize async WebSocket public client
        
        Args:
            on_message: Async callback function for messages
            on_error: Async callback function for errors
            on_close: Async callback function for connection close
            on_open: Async callback function for connection open
        """
        super().__init__()
        self.ws = None
        self.on_message_callback = on_message
        self.on_error_callback = on_error
        self.on_close_callback = on_close
        self.on_open_callback = on_open
        self._running = False

    async def connect(self):
        """
        Establish WebSocket connection and start listening
        """
        try:
            self.ws = await websockets.connect(self.get_ws_url())
            self._running = True
            
            if self.on_open_callback:
                if asyncio.iscoroutinefunction(self.on_open_callback):
                    await self.on_open_callback()
                else:
                    self.on_open_callback()
            
            await self._listen()
        except Exception as e:
            if self.on_error_callback:
                if asyncio.iscoroutinefunction(self.on_error_callback):
                    await self.on_error_callback(e)
                else:
                    self.on_error_callback(e)

    async def _listen(self):
        """Listen for incoming messages"""
        try:
            async for message in self.ws:
                if self.on_message_callback:
                    try:
                        data = json.loads(message)
                        if asyncio.iscoroutinefunction(self.on_message_callback):
                            await self.on_message_callback(data)
                        else:
                            self.on_message_callback(data)
                    except json.JSONDecodeError:
                        if asyncio.iscoroutinefunction(self.on_message_callback):
                            await self.on_message_callback(message)
                        else:
                            self.on_message_callback(message)
        except websockets.exceptions.ConnectionClosed as e:
            if self.on_close_callback:
                if asyncio.iscoroutinefunction(self.on_close_callback):
                    await self.on_close_callback(e.code, e.reason)
                else:
                    self.on_close_callback(e.code, e.reason)
        except Exception as e:
            if self.on_error_callback:
                if asyncio.iscoroutinefunction(self.on_error_callback):
                    await self.on_error_callback(e)
                else:
                    self.on_error_callback(e)
        finally:
            self._running = False

    async def send(self, message: Dict[str, Any]):
        """
        Send message to WebSocket server
        
        Args:
            message: Message dict to send
        """
        if self.ws and not self.ws.closed:
            await self.ws.send(json.dumps(message))

    async def subscribe(self, subscription_message: Dict[str, Any]):
        """
        Subscribe to a stream
        
        Args:
            subscription_message: Subscription message from base class methods
        """
        await self.send(subscription_message)

    async def close(self):
        """
        Close WebSocket connection
        """
        self._running = False
        if self.ws and not self.ws.closed:
            await self.ws.close()
