import asyncio
import websockets

from shared_constants import SERVER_IP, SERVER_PORT


async def send_message(ciphertext):
    async with websockets.connect(f"ws://{SERVER_IP}:{SERVER_PORT}") as websocket:
        await websocket.send(ciphertext)
        response = await websocket.recv()
        return response


async def main():
    while True:
        ciphertext = input(
            "Enter base64 encoded ciphertext to send to the server (or 'q' to exit): "
        )
        if ciphertext == "q":
            break

        response = await send_message(f"CONSOLE:{ciphertext}")
        print(f"Server response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
