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

MESSAGE = b"Throughout the ages, civilizations have risen and fallen, each leaving behind echoes of their existence, traces of their once-great empires scattered across the pages of history. The ancient cities, now buried under layers of earth, speak of cultures that thrived in ways we can only imagine, of peoples who knew the secrets of the stars and whose knowledge rivaled the greatest minds of today. These cities, with their faded murals and crumbling walls, serve as silent reminders of a world lost to time. Legends tell of vast libraries filled with scrolls of wisdom, of marketplaces brimming with the finest goods from across the lands, and of grand temples that reached toward the heavens. The stories of their kings and queens, their warriors and poets, survive in the fragments we uncover, painting a picture of a world both strange and familiar. Yet, for all our knowledge, there remains much that is hidden, mysteries locked away in the shadows of antiquity. In the distant sands of forgotten deserts, under the canopy of ancient forests, and atop mountains that pierce the sky, remnants of these lost eras wait to be discovered. And for every artifact unearthed, for every ruin explored, there are countless more that remain unseen, waiting for the day when they will once again feel the light of day. For those who dare to seek them, the rewards are more than mere riches; they are the answers to questions as old as humanity itself.In this endless quest for knowledge, we are united by our shared curiosity, our relentless pursuit of understanding. The world is vast, and our journey has only just begun."
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
    encrypted_ciphertext = block_cipher.encrypt(padded_plaintext)

    ciphertext = b64encode(encrypted_ciphertext)
    print(f"Encoded Ciphertext: {ciphertext}")

    socketserver.TCPServer.allow_reuse_address = True
    server = TCPServer((SERVER_IP, SERVER_PORT), ChallengeRequestHandler)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

    print(
        f"[DEBUG] KEY: {KEY.hex()}, KEY length: {len(KEY)}, IV: {IV}, IV length: {len(IV)}"
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
