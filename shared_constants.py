from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Constants for the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 4444

# Constants for encryption/decryption
IV = get_random_bytes(AES.block_size)

# Constants for the server response
CORRECT_MESSAGE = b"200 Correct message"
INVALID_PADDING = b"400 Invalid padding"
INVALID_MESSAGE = b"401 Invalid message"
