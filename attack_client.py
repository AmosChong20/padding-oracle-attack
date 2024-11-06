import socket
from base64 import b64encode, b64decode
import asyncio
import websockets

from Crypto.Cipher import AES

from shared_constants import SERVER_IP, SERVER_PORT, INVALID_PADDING
from Crypto.Util.Padding import unpad

# Attacker to fill in the following values
CIPHERTEXT =  b'zU6LuKf4JzcWeF7N6iS6SFvHEKN/RPPtfI1gRKGSGm4='
IV = b'\x8f\xc6\x19\x80\xf5\xa3\xcbtj\xae\x10\x11\xdd\xec\x7f\xfe'

BLOCK_SIZE = AES.block_size


async def send_and_receive(ciphertext):
    async with websockets.connect(f"ws://{SERVER_IP}:{SERVER_PORT}") as websocket:
        await websocket.send(b64encode(ciphertext).decode())
        response = await websocket.recv()
        return response


async def padding_oracle_attack(iv, ciphertext):
    blocks = [iv] + [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    print(f"Blocks: {blocks}")
    decrypted_message = b''

    for block_index in range(len(blocks) - 1):
        print(f"Block index: {block_index}")
        current_iv = blocks[block_index]
        target_block = blocks[block_index + 1]
        decrypted_block = bytearray(BLOCK_SIZE)
        keystream_block = bytearray(BLOCK_SIZE)

        for byte_index in range(1, BLOCK_SIZE + 1):
            padding_value = byte_index

            for guess_byte in range(256):
                forged_iv = bytearray(b"\x00" * BLOCK_SIZE)

                for i in range(1, byte_index):
                    forged_iv[-i] = keystream_block[-i] ^ padding_value

                forged_iv[-byte_index] = guess_byte
                response = await send_and_receive(bytes(forged_iv) + target_block)
                if response != INVALID_PADDING:
                    keystream_byte = forged_iv[-byte_index] ^ padding_value
                    keystream_block[-byte_index] = keystream_byte
                    decrypted_byte = keystream_byte ^ current_iv[-byte_index]
                    decrypted_block[-byte_index] = decrypted_byte
                    print(f"Plaintext block: {decrypted_block}")
                    break
        decrypted_message += decrypted_block

    return decrypted_message


async def main():
    # Decode base64 ciphertext received from the server
    decoded_ciphertext = b64decode(CIPHERTEXT)
    
    # Use padding oracle attack to retrieve the plaintext
    plaintext = await padding_oracle_attack(IV, decoded_ciphertext)

    print(f"Decrypted message: {plaintext}")
    # Connect to the server
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     print(f"Connecting to {SERVER_IP}:{SERVER_PORT}")
    #     sock.connect((SERVER_IP, SERVER_PORT))

    #     # Ciphertext of the known message padded and encrypted with server's key
    #     ciphertext = CIPHERTEXT
    #     iv = IV

    #     # Decode base64 ciphertext received from the server
    #     decoded_ciphertext = b64decode(ciphertext)
        
    #     # Use padding oracle attack to retrieve the plaintext
    #     plaintext = padding_oracle_attack(sock, iv, decoded_ciphertext)

    #     print(f"Decrypted message: {plaintext}")


if __name__ == "__main__":
    asyncio.run(main())
