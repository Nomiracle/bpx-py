from bpx.ws_public import WsPublic
import asyncio


async def on_message(message):
    print(f"收到消息: {message}")


async def on_error(error):
    print(f"错误: {error}")


async def on_close(status_code, msg):
    print(f"连接关闭: {status_code} - {msg}")


async def on_open():
    print("WebSocket连接已建立")


async def main():
    # 创建公共WebSocket客户端
    ws_client = WsPublic(
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # 创建连接任务
    connect_task = asyncio.create_task(ws_client.connect())
    
    # 等待连接建立
    await asyncio.sleep(1)
    
    # 订阅SOL_USDC的ticker
    await ws_client.subscribe(ws_client.subscribe_ticker("SOL_USDC"))
    
    # 订阅深度数据
    await ws_client.subscribe(ws_client.subscribe_depth("SOL_USDC"))
    
    # 订阅交易数据
    await ws_client.subscribe(ws_client.subscribe_trades("SOL_USDC"))
    
    # 保持运行30秒
    try:
        await asyncio.sleep(30)
    except KeyboardInterrupt:
        print("\n正在关闭连接...")
    finally:
        await ws_client.close()
        await connect_task


if __name__ == "__main__":
    asyncio.run(main())
