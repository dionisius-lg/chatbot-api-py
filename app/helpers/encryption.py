from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from app.config import secret
from app.helpers.value import is_empty

iv = "initVector16Bits"

def encrypt(value: str) -> str|None:
    try:
        if not isinstance(secret, str) or len(secret) != 32:
            raise ValueError("Secret key must be 32 bytes for AES-256 encryption")
        if not isinstance(value, str) or is_empty(value):
            raise ValueError("Value must be string and cannot be empty")

        # pad the plaintext to be a multiple of AES's block size (16 bytes)
        padder = padding.PKCS7(128).padder() # 128-bit block size for AES
        padded_data = padder.update(value.encode()) + padder.finalize()

        # create the cipher object for encryption
        cipher = Cipher(algorithms.AES(secret.encode()), modes.CBC(iv.encode()), backend=default_backend())
        encryptor = cipher.encryptor()

        # encrypt the padded data
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # return the encrypted data in hexadecimal format
        return encrypted.hex()
    except Exception as e:
        return None

def decrypt(value: str) -> str|None:
    try:
        if not isinstance(secret, str) or len(secret) != 32:
            raise ValueError("Secret key must be 32 bytes for AES-256 encryption")
        if not isinstance(value, str) or is_empty(value):
            raise ValueError("Value must be string and cannot be empty")

        # convert the hex string back to bytes
        encrypted_data = bytes.fromhex(value)

        # create the cipher object for decryption
        cipher = Cipher(algorithms.AES(secret.encode()), modes.CBC(iv.encode()), backend=default_backend())
        decryptor = cipher.decryptor()

        # decrypt the data
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        # unpad the decrypted data to get the original message
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

        # return the decrypted data as a string
        return decrypted_data.decode()
    except Exception as e:
        return None
