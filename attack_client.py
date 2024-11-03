import socket
from base64 import b64encode, b64decode
from shared_constants import SERVER_IP, SERVER_PORT, IV, INVALID_PADDING
from Crypto.Util.Padding import unpad

BLOCK_SIZE = 16

CIPHERTEXT = b'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'
IV = b'\xa6\xbc\xfa\xf7Ji\xcc\x1a\xd8\xec\x1b\xda\x88H\x0b\xa4'

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
        sock.connect((SERVER_IP, SERVER_PORT))

        # Ciphertext of the known message padded and encrypted with server's key
        ciphertext = CIPHERTEXT
        iv = IV

        # Decode base64 ciphertext received from the server
        decoded_ciphertext = b64decode(ciphertext)
        
        # Use padding oracle attack to retrieve the plaintext
        plaintext = padding_oracle_attack(sock, iv, decoded_ciphertext)
        
        print(f"Decrypted message: {unpad(plaintext, BLOCK_SIZE)}")

if __name__ == "__main__":
    main()
