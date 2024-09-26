import asyncio
import websockets

connected_clients = set()


async def handle_client(websocket, path):
    # Đăng ký client mới
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Nhận được tin nhắn: {message}")
            # Phát tin nhắn tới tất cả các client đã kết nối, trừ người gửi
            await broadcast(message, websocket)
    except websockets.ConnectionClosed:
        print("Client ngắt kết nối")
    finally:
        # Gỡ client khi ngắt kết nối
        connected_clients.remove(websocket)


async def broadcast(message, sender):
    if connected_clients:  # Kiểm tra nếu có client đã kết nối
        tasks = [
            asyncio.create_task(client.send(message))
            for client in connected_clients
            if client != sender  # Chỉ gửi tin nhắn đến những client khác
        ]
        if tasks:  # Kiểm tra xem tasks có trống không
            await asyncio.wait(tasks)


async def start_server():
    print("WebSocket server đang chạy trên ws://0.0.0.0:3000")
    async with websockets.serve(handle_client, "0.0.0.0", 3000):
        await asyncio.Future()  # Chạy mãi mãi


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Server đã dừng.")
