from cryptography.hazmat.primitives.asymmetric import ed25519
import base64
from typing import Dict, Any, List, Optional
from time import time


class BaseWsAccount:
    """
    Base class for authenticated WebSocket connections
    Provides methods to generate subscription messages for private streams
    """

    WS_URL = "wss://ws.backpack.exchange/"

    def __init__(self, public_key: str, secret_key: str, window: int = 5000, debug: bool = False):
        """
        Initialize the base WebSocket account
        
        Args:
            public_key: API public key
            secret_key: API secret key (base64 encoded)
            window: Time window for signature validity in milliseconds
            debug: Enable debug mode
        """
        self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(secret_key)
        )
        self.public_key = public_key
        self.window = window
        self.debug = debug

    def get_ws_url(self) -> str:
        """
        Returns the WebSocket URL for authenticated streams
        """
        return self.WS_URL

    def get_auth_message(self) -> Dict[str, Any]:
        """
        Generate authentication message for WebSocket connection
        
        Returns:
            Authentication message dict
        """
        timestamp = int(time() * 1e3)
        signature = self._sign_ws_auth(timestamp)
        
        return {
            "method": "SUBSCRIBE",
            "params": ["account.orderUpdate"],
            "signature": signature,
            "timestamp": timestamp,
            "window": self.window,
            "apiKey": self.public_key
        }

    def subscribe_order_update(self) -> Dict[str, Any]:
        """
        Subscribe to order updates
        
        Returns:
            Subscription message dict with authentication
        """
        timestamp = int(time() * 1e3)
        signature = self._sign_ws_auth(timestamp)
        
        return {
            "method": "SUBSCRIBE",
            "params": ["account.orderUpdate"],
            "signature": signature,
            "timestamp": timestamp,
            "window": self.window,
            "apiKey": self.public_key
        }

    def subscribe_fill_update(self) -> Dict[str, Any]:
        """
        Subscribe to fill/trade updates
        
        Returns:
            Subscription message dict with authentication
        """
        timestamp = int(time() * 1e3)
        signature = self._sign_ws_auth(timestamp)
        
        return {
            "method": "SUBSCRIBE",
            "params": ["account.fillUpdate"],
            "signature": signature,
            "timestamp": timestamp,
            "window": self.window,
            "apiKey": self.public_key
        }

    def subscribe_balance_update(self) -> Dict[str, Any]:
        """
        Subscribe to balance updates
        
        Returns:
            Subscription message dict with authentication
        """
        timestamp = int(time() * 1e3)
        signature = self._sign_ws_auth(timestamp)
        
        return {
            "method": "SUBSCRIBE",
            "params": ["account.balanceUpdate"],
            "signature": signature,
            "timestamp": timestamp,
            "window": self.window,
            "apiKey": self.public_key
        }

    def subscribe_position_update(self) -> Dict[str, Any]:
        """
        Subscribe to position updates
        
        Returns:
            Subscription message dict with authentication
        """
        timestamp = int(time() * 1e3)
        signature = self._sign_ws_auth(timestamp)
        
        return {
            "method": "SUBSCRIBE",
            "params": ["account.positionUpdate"],
            "signature": signature,
            "timestamp": timestamp,
            "window": self.window,
            "apiKey": self.public_key
        }

    def unsubscribe(self, streams: List[str]) -> Dict[str, Any]:
        """
        Unsubscribe from specific streams
        
        Args:
            streams: List of stream names to unsubscribe from
        
        Returns:
            Unsubscribe message dict
        """
        timestamp = int(time() * 1e3)
        signature = self._sign_ws_auth(timestamp)
        
        return {
            "method": "UNSUBSCRIBE",
            "params": streams,
            "signature": signature,
            "timestamp": timestamp,
            "window": self.window,
            "apiKey": self.public_key
        }

    def _sign_ws_auth(self, timestamp: int) -> str:
        """
        Sign WebSocket authentication message
        
        Args:
            timestamp: Current timestamp in milliseconds
        
        Returns:
            Base64 encoded signature
        """
        sign_str = f"instruction=subscribe&timestamp={timestamp}&window={self.window}"
        
        if self.debug:
            print(f"WS Sign String: {sign_str}")
        
        signature_bytes = self.private_key.sign(sign_str.encode())
        encoded_signature = base64.b64encode(signature_bytes).decode()
        
        return encoded_signature
