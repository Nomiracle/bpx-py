from typing import List, Optional, Dict, Any


class BaseWsPublic:
    """
    Base class for public WebSocket connections
    Provides methods to generate subscription messages for public streams
    """

    WS_URL = "wss://ws.backpack.exchange/"

    def get_ws_url(self) -> str:
        """
        Returns the WebSocket URL for public streams
        """
        return self.WS_URL

    def subscribe_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Subscribe to ticker updates for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., "SOL_USDC")
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": [f"ticker.{symbol}"]
        }

    def subscribe_tickers(self) -> Dict[str, Any]:
        """
        Subscribe to ticker updates for all symbols
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": ["tickers"]
        }

    def subscribe_depth(self, symbol: str) -> Dict[str, Any]:
        """
        Subscribe to order book depth updates for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., "SOL_USDC")
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": [f"depth.{symbol}"]
        }

    def subscribe_klines(self, symbol: str, interval: str) -> Dict[str, Any]:
        """
        Subscribe to kline/candlestick updates for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., "SOL_USDC")
            interval: Kline interval (e.g., "1m", "5m", "1h", "1d")
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": [f"kline.{symbol}.{interval}"]
        }

    def subscribe_trades(self, symbol: str) -> Dict[str, Any]:
        """
        Subscribe to recent trades for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., "SOL_USDC")
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": [f"trades.{symbol}"]
        }

    def subscribe_mark_price(self, symbol: str) -> Dict[str, Any]:
        """
        Subscribe to mark price updates for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., "SOL_USDC")
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": [f"markPrice.{symbol}"]
        }

    def subscribe_mark_prices(self) -> Dict[str, Any]:
        """
        Subscribe to mark price updates for all symbols
        
        Returns:
            Subscription message dict
        """
        return {
            "method": "SUBSCRIBE",
            "params": ["markPrices"]
        }

    def unsubscribe(self, streams: List[str]) -> Dict[str, Any]:
        """
        Unsubscribe from specific streams
        
        Args:
            streams: List of stream names to unsubscribe from
        
        Returns:
            Unsubscribe message dict
        """
        return {
            "method": "UNSUBSCRIBE",
            "params": streams
        }
