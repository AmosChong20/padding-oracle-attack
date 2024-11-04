import socket
from base64 import b64encode, b64decode

from Crypto.Cipher import AES

from shared_constants import SERVER_IP, SERVER_PORT, INVALID_PADDING
from Crypto.Util.Padding import unpad

# Attacker to fill in the following values
CIPHERTEXT = b'2Q2f0WM3vBm8iyAjr11p9uzBcvkUIal1Kkp6s3cXAYfSA2n65AMJ8xwQk0xB5kZ4f8KyhMomnwJ9SEiLc3XTyVOiBeoghybo3IK6kR+ZSMRGksQDjUy05ZMtf35696/N0tJQqwnyVL/WG8BfWHVA99jTYJk7kO6esGF5VB/o+VzNVif8DPyvsLt0awwlMhJ0Bkn5KdXAdAT6wyIgblQEZcWqOPx6zQJkaKjML5FYHBe30Z473xSg1N2Z75rHSJc/qDtW17o2fR2wzJuWsOIkvoeRO5PaHhgU9zd7l2R/3PbKmB8RFwRJvOC3MOIgigXtauddnAhUFptgg8gHAHs+eqNqi7XVz7xUYz9FMb1aeTQ1dy7dX8luSGRnqHfxaj332ktbZpWyvHWIrnDBZjtp3yBWv0NlHy/p0ut+UboNM2mR41nr1czvNkUUBIde8f20CmtZatTFL+AUDMIAe4baA7Kd6bUjqLv4xPQIz44wf9BVMqnwsOckiAY+Xlug2FX8wRj4x06c2nB3ruxXzHKcW12nZJlJYg6RlUY2ndvYvG2HlP5Aq/HWKGdlOCGxLfyL+FPbg7+R7HoZiNw8laybsEWmAQJysHNvu4ARL4f95JQZYvvMplGedHmp65ASAVU/b6KPSeHgs23Jlqp31plSVcieg8PxggAgVWdPGmju7MlRTO6d8ZN6IR2UlE7QzDNSSmpe0wU7QdixP5phGBGCQlYUTRyf7pQnbjP2W8sTiR+2eSIwCOYUE2Q9f4j9yTlj7RglnHR1qMaj3F2Xw+jvKSiLBDYKhh54TRcaoKNxhqgCPoGjwytUbBaWa6u/Ytk8TKSA//o2+cpZ0U8E03GhVfyj+Hu5/Xwm5Gv/8O1ywZyW2YypvRwYu6Dk+MqfCqNlmlXjsqJjt2letByB5vl713pObyNQsAZ5n9stk4eL+FV7Jr62EWodUOlcX0sNy09w7W1l/eSxRVYKnJp5wNlr3VMsWUTlvFd2iU1jjrw1CNZ38wme7nppxkOF/g9VDRU7QtNcZq4AIMUb/XJ88gSRPsDBPzuTAVCvQYkB8gfEZyNITNur+GbUcsxAEczpDZaE7abuKZeGPUjhd5xcca4hF59tRLnHPdD+CCukmc4bTrWBrKWPNLZPf9OkVSLsAdQYJzixXaTzEMwKeNHUqtFtOVOYXNyzMV2O6YbXbgfJ3n8TwQREI6ZBiZ1F6MSoA4ZMXtGThDS5Zx8NRmZzJHaHC2aL7r+Ca+FzhKs00D+4oM4GOTs50ZmzUdstUMd+aytErC3duiCPK8kI9OCei6h8lgu1t3lBkt1hoVCvNzqNGWy/B9eIDxVe2l5dJtnai/uVDS5+SH2WclCAuq/cV90pap4wi1fcgYxdg4S3h7zdT6m+SR28YB3y/ldQxZD7EP5S+QGQz3jI8NX4P8sW0u/JwHwJeBWQNZgsYp52iHCUWkbGlhYzI1RQ7mydOBVgXrXNxY/TIJMWM0kTsvnjVk5PbJ+rqzZuHrdfvcCO1xgV8o/WDRYgp3Gf3Gup0YtaJUpukPGYygCPjP3Vbes7eqNFta079CRRWXMXaBXOfRR6jmHLcUgy1e/OkafwPmObwQD2b/6dDqEWsvmLz1jEKZIfQWmwtfNmVQjpUPIi+jz9Krp4cBgwni0S3NCIDRT7lwiN6YjtOzWIBtAyb9NEV1GnltNex6T2CmHYvHmE93CgBLMw2DfDDuEuwTMyM95ToHRytK76DtUJpVZLte5jFzMEJOV0QKEaWst+OTX6Rn4liB2M3nTD+Cgvv+QplwV9JESFZYXeUeyKvY7F5L0o05k9EiGClmUJQs/IuhEZ9It1BNdT8lBhzh5syaLRNyLuw83n1FADpeFeomWvJKSJVrXiB5WndG8wM9yVd6vRqS9aWt0VZr4F8F9+wlnKM6nyaZQOme93yqm1r33+yM3VClJl+9RpCTANUhV8rf8Bxru/GW2n9i9xGOA2BNU92XoTHp0rmUdAKaEP8msNzvMxTObon7mzpNhKiXk70Owf46qPJ4yUEkPg/Dc27QUiXer+mOjCS3LruEGktmTqkpTQ0paXxbnU9RBe7cgbcCzmUSvwdSexnCNMFBLj1BwQGErNqfiQaGHHila0DQ11I3QgVfbn4rkCDFwDUhPn5B0W0lV+I3w='
IV = b'\x8e\x1f\xab\x86\xe0\x99\xda\xf5\xf3\r\xb5.\x93!\xe3w'

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
                forged_iv = bytearray(b"\x00" * BLOCK_SIZE)

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

        print(f"Decrypted message: {unpad(plaintext, BLOCK_SIZE)}")


if __name__ == "__main__":
    main()
