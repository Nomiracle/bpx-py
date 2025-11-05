from bpx.ws_account import WsAccount
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
    # 替换为你的API密钥
    public_key = "<YOUR_PUBLIC_KEY>"
    secret_key = "<YOUR_SECRET_KEY>"
    
    # 创建账户WebSocket客户端
    ws_client = WsAccount(
        public_key=public_key,
        secret_key=secret_key,
        window=5000,
        debug=False,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # 创建连接任务
    connect_task = asyncio.create_task(ws_client.connect())
    
    # 等待连接建立
    await asyncio.sleep(1)
    
    # 订阅订单更新
    await ws_client.subscribe(ws_client.subscribe_order_update())
    
    # 订阅成交更新
    await ws_client.subscribe(ws_client.subscribe_fill_update())
    
    # 订阅余额更新
    await ws_client.subscribe(ws_client.subscribe_balance_update())
    
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
