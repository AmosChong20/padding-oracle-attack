from base64 import b64encode, b64decode
import asyncio
import websockets

from Crypto.Cipher import AES

from shared_constants import SERVER_IP, SERVER_PORT, INVALID_PADDING
from Crypto.Util.Padding import unpad

# Attacker to fill in the following values
CIPHERTEXT =  b'03MdZ2FPUDXoVrVQh17vgqiak7Es1Sax+juuxCdLLzWJrNLEeYxcQN60W1f0aZQI'
IV = b'\x0e\x8e\xd8\xba\xc7\xea\x04Y\xe0\xf7\xb32\xc5>;\xf9'

BLOCK_SIZE = AES.block_size


async def send_and_receive(websocket, ciphertext):
    await websocket.send(b64encode(ciphertext).decode())
    response = await websocket.recv()
    return response


async def padding_oracle_attack(iv, ciphertext):
    timeout = 10
    async with websockets.connect(
        f"ws://{SERVER_IP}:{SERVER_PORT}",
        open_timeout=timeout,  # Timeout for opening the connection
        ping_timeout=timeout 
    ) as websocket:
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
                    response = await send_and_receive(websocket, bytes(forged_iv) + target_block)
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

    print(f"Decrypted message: {unpad(plaintext, BLOCK_SIZE)}")


if __name__ == "__main__":
    asyncio.run(main())
