import socket
from base64 import b64encode, b64decode

from Crypto.Cipher import AES

from shared_constants import SERVER_IP, SERVER_PORT, INVALID_PADDING
from Crypto.Util.Padding import unpad

# Attacker to fill in the following values
CIPHERTEXT = b"0/piYc4LLuupxcoKqToB0JDsY41FAtFIRpKTTT2yKSg="
IV = b"\xees\xfaFQ\xcd\x89\xc3\xcck\x97\xccW\xb3]\xe1"

BLOCK_SIZE = AES.block_size


def send_and_receive(sock, ciphertext):
    sock.sendall(b64encode(ciphertext))
    response = sock.recv(4096)
    return response


def padding_oracle_attack(sock, iv, ciphertext):
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
                forged_iv = bytearray(current_iv)

                for i in range(1, byte_index):
                    forged_iv[-i] = keystream_block[-i] ^ padding_value

                forged_iv[-byte_index] = guess_byte
                response = send_and_receive(sock, bytes(forged_iv) + target_block)
                if response != INVALID_PADDING:
                    keystream_byte = forged_iv[-byte_index] ^ padding_value
                    keystream_block[-byte_index] = keystream_byte
                    decrypted_byte = keystream_byte ^ current_iv[-byte_index]
                    decrypted_block[-byte_index] = decrypted_byte
                    print(f"Plaintext block: {decrypted_block}")
                    break
        decrypted_message += decrypted_block

    return decrypted_message


def main():
    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}")
        sock.connect((SERVER_IP, SERVER_PORT))

        # Ciphertext of the known message padded and encrypted with server's key
        ciphertext = CIPHERTEXT
        iv = IV

        # Decode base64 ciphertext received from the server
        decoded_ciphertext = b64decode(ciphertext)
        
        # Use padding oracle attack to retrieve the plaintext
        plaintext = padding_oracle_attack(sock, iv, decoded_ciphertext)

        print(f"plaintext: {plaintext}")
        print(f"Decrypted message: {unpad(plaintext, BLOCK_SIZE)}")


if __name__ == "__main__":
    main()
