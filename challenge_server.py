import socketserver
from base64 import b64decode, b64encode
from socket import socket

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad

from shared_constants import (
    IV,
    SERVER_IP,
    SERVER_PORT,
    CORRECT_MESSAGE,
    INVALID_PADDING,
    INVALID_MESSAGE,
)

MESSAGE = b"A" * 16 + b"[The actual message here]"
KEY = get_random_bytes(AES.block_size)


class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ChallengeRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            challenge(self.request)


def challenge(req: socket):
    while True:
        try:
            ciphertext = req.recv(4096)
            if not ciphertext:
                # Exit the loop if no data is received (client disconnected)
                break

            ciphertext = b64decode(ciphertext)
            padded_plaintext = AES.new(KEY, AES.MODE_CBC, IV).decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, AES.block_size)
            # print(f"Received plaintext: {plaintext}")

            if plaintext == MESSAGE:
                # Send OK if the decrypted message is the same as the original message
                req.sendall(CORRECT_MESSAGE)
            else:
                # Send Unauthorized if the decrypted message is different from the original message
                req.sendall(INVALID_MESSAGE)

        except ValueError as e:
            # Send Invalid padding if the padding is incorrect
            req.sendall(INVALID_PADDING)

        except Exception as e:
            print(e)
            break


def main():
    print(f"Plaintext: {MESSAGE}")
    padded_plaintext = pad(MESSAGE, AES.block_size)
    print(f"Padded plaintext: {padded_plaintext}")

    block_cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ciphertext = b64encode(block_cipher.encrypt(padded_plaintext))
    print(f"Ciphertext: {ciphertext}")

    socketserver.TCPServer.allow_reuse_address = True
    server = TCPServer((SERVER_IP, SERVER_PORT), ChallengeRequestHandler)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    print(
        f"[DEBUG] KEY: {KEY.hex()}, KEY length: {len(KEY)}, IV: {IV.hex()}, IV length: {len(IV)}"
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
