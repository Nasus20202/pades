"""!
@package crypt
This module contains cryptographic functions for hashing, RSA key generation, AES encryption and decryption.
"""

import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import Crypto.Cipher.AES as AES


def hash_string(string: str) -> str:
    """!
    Hash a string using SHA256.

    @param string: The string to hash.

    @return The hashed string."""
    return SHA256.new(string.encode("utf-8")).digest()


def generate_rsa_key_pair(key_size: int = 4096) -> tuple[bytes, bytes]:
    """!
    Generate a RSA key pair.

    @param key_size: The size of the key in bits.

    @return A tuple containing the private and public key."""
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_data_with_aes(data: bytes, key: bytes) -> bytes:
    """!
    Encrypt data using AES.

    @param data: The data to encrypt.
    @param key: The key to use for encryption.

    @return The encrypted data."""
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, tag, ciphertext


def decrypt_data_with_aes(
    nonce: bytes, tag: bytes, ciphertext: bytes, key: bytes
) -> bytes:
    """!
    Decrypt data using AES.

    @param nonce: The nonce used for encryption.
    @param tag: The tag used for encryption.
    @param ciphertext: The encrypted data.
    @param key: The key to use for decryption.

    @return The decrypted data."""
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def merge_cipher_data(nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    """!
    Merge the nonce, tag and ciphertext into a single byte string.

    @return The merged data."""
    return nonce + tag + ciphertext


def split_cipher_data(data: bytes) -> tuple[bytes, bytes, bytes]:
    """!
    Split the merged data into the nonce, tag and ciphertext.

    @return A tuple containing the nonce, tag and ciphertext."""
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    return nonce, tag, ciphertext
