import asyncio
import websockets
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from shared_constants import (
    SERVER_IP,
    SERVER_PORT,
    CORRECT_MESSAGE,
    INVALID_PADDING,
    INVALID_MESSAGE,
)

# Configuration for the server
MESSAGE = b"Hello, this is a test message!"
KEY = get_random_bytes(AES.block_size)
IV = get_random_bytes(AES.block_size)

print(
    f"[DEBUG] KEY: {KEY}, IV: {IV}, KEY hex: {KEY.hex()}, IV hex: {IV.hex()}, MESSAGE length: {len(MESSAGE)}"
)


async def handle_connection(websocket):
    while True:
        try:
            data = await websocket.recv()
            if not data:
                break
            if data.startswith("ENCRYPT:"):
                # Call the encryption function when client sends a special "ENCRYPT" request
                message_to_encrypt = data[len("ENCRYPT:") :].strip()
                encrypted_message = encrypt_message(message_to_encrypt)
                await websocket.send(encrypted_message)
            else:
                # Decrypt the received ciphertext if not an "ENCRYPT" request
                ciphertext = data.encode("utf-8")
                decrypted_message = decrypt_message(ciphertext)
                await websocket.send(decrypted_message)

        except Exception as e:
            break


def encrypt_message(message: str) -> str:
    padded_plaintext = pad(message.encode("utf-8"), AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(padded_plaintext)
    ciphertext = b64encode(encrypted).decode("utf-8")
    return ciphertext


def decrypt_message(ciphertext: bytes) -> bytes:
    try:
        ciphertext = b64decode(ciphertext)
        padded_plaintext = AES.new(KEY, AES.MODE_CBC, IV).decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        return plaintext

        # if plaintext == MESSAGE:
        #     # Send OK if the decrypted message is the same as the original message
        #     return CORRECT_MESSAGE
        # else:
        #     # Send Unauthorized if the decrypted message is different from the original message
        #     return INVALID_MESSAGE

    except ValueError:
        # Send Invalid padding if the padding is incorrect
        return INVALID_PADDING

    except Exception as e:
        print(f"Decryption error: {e}")
        return INVALID_MESSAGE


async def main():
    # Start the WebSocket server
    padded_plaintext = pad(MESSAGE, AES.block_size)
    # print(f"Padded plaintext: {padded_plaintext}")

    block_cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_ciphertext = block_cipher.encrypt(padded_plaintext)

    ciphertext = b64encode(encrypted_ciphertext)
    print(f"Encoded Ciphertext: {ciphertext}")

    server = await websockets.serve(handle_connection, SERVER_IP, SERVER_PORT)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
