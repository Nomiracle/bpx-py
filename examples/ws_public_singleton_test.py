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
    # 创建第一个实例
    ws_client1 = WsPublic(
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # 创建第二个实例（应该返回同一个实例）
    ws_client2 = WsPublic()
    
    # 验证是同一个实例
    print(f"ws_client1 和 ws_client2 是同一个实例: {ws_client1 is ws_client2}")
    print(f"ws_client1 ID: {id(ws_client1)}")
    print(f"ws_client2 ID: {id(ws_client2)}")
    
    # 创建连接任务（只会建立一次连接）
    connect_task = asyncio.create_task(ws_client1.connect())
    
    # 等待连接建立
    await asyncio.sleep(1)
    
    # 使用第一个实例订阅
    await ws_client1.subscribe(ws_client1.subscribe_ticker("SOL_USDC"))
    
    # 使用第二个实例订阅（使用同一个连接）
    await ws_client2.subscribe(ws_client2.subscribe_depth("SOL_USDC"))
    
    # 保持运行10秒
    try:
        await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("\n正在关闭连接...")
    finally:
        await ws_client1.close()
        await connect_task


if __name__ == "__main__":
    asyncio.run(main())
