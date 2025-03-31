## @file key_management.py
# This module contains functions related to key management.
import os

from lib.crypt import *

## @var PRIVATE_KEY_DIR
# The directory where the private key is stored on the device.
PRIVATE_KEY_DIR = ""
## @var PRIVATE_KEY_FILENAME
# The filename of the private key.
PRIVATE_KEY_FILENAME = "private_key.pem"
## @var ENCRYPTED_EXTENSION
# The extension of the encrypted private key.
ENCRYPTED_EXTENSION = ".aes"
## @var PUBLIC_KEY_DIR
# The directory where the public key is stored (current working directory).
PUBLIC_KEY_DIR: str = os.getcwd()
## @var PUBLIC_KEY_FILENAME
# The filename of the public key.
PUBLIC_KEY_FILENAME = "public_key.pub"


def generate_and_save_keys(device_path: str, pin: str) -> tuple[str, str]:
    """!
    Generate a RSA key pair and save it to the @ref PUBLIC_KEY_DIR and the private key to the device_path.

    @param device_path: The path to the device where the private key should be saved.
    @param pin: The pin to encrypt the private key with.

    @return A tuple containing the path to the private key and the path to the public key.
    """
    private_key, public_key = generate_rsa_key_pair()
    return (
        encrypt_and_save_private_key(pin, device_path, private_key),
        save_public_key(public_key),
    )


def encrypt_and_save_private_key(pin: str, device_path: str, private_key: bytes) -> str:
    """!
    Encrypt the private key with the pin and save it to the device_path.

    @param pin: The pin to encrypt the private key with.
    @param device_path: The path to the device where the private key should be saved.
    @param private_key: The private key to encrypt and save.

    @return The path to the private key.
    """
    aes_key = hash_string(pin)
    private_key_nonce, private_key_tag, encrypted_private_key = encrypt_data_with_aes(
        private_key, aes_key
    )

    private_key_path = (
        f"{device_path}/{PRIVATE_KEY_DIR}{PRIVATE_KEY_FILENAME}{ENCRYPTED_EXTENSION}"
    )
    with open(
        private_key_path,
        "wb",
    ) as file:
        file.write(
            merge_cipher_data(private_key_nonce, private_key_tag, encrypted_private_key)
        )
    return private_key_path


def save_public_key(public_key: bytes) -> str:
    """!
    Save the public key to the @ref PUBLIC_KEY_DIR under @ref PUBLIC_KEY_FILENAME name.

    @param public_key: The public key to save.

    @return The path to the public key.
    """
    public_key_path = f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}"
    with open(
        public_key_path,
        "wb",
    ) as file:
        file.write(public_key)
    return public_key_path


def read_and_decrypt_private_key(pin: str, device_path: str) -> bytes:
    """!
    Read the private key from the device_path and decrypt it with the pin.
    The filename of the private key is @ref PRIVATE_KEY_FILENAME with @ref ENCRYPTED_EXTENSION.

    @param pin: The pin to decrypt the private key with.
    @param device_path: The path to the device where the private key is stored.

    @return The decrypted private key or None when there is an error opening the private key file.
    """
    aes_key = hash_string(pin)
    with open(
        f"{device_path}/{PRIVATE_KEY_DIR}{PRIVATE_KEY_FILENAME}{ENCRYPTED_EXTENSION}",
        "rb",
    ) as file:
        data = file.read()
        private_key_nonce, private_key_tag, encrypted_private_key = split_cipher_data(
            data
        )
        return decrypt_data_with_aes(
            private_key_nonce, private_key_tag, encrypted_private_key, aes_key
        )
    return None


def read_public_key(path: str = None) -> bytes:
    """!
    Read the public key from the path.
    The default path is @ref PUBLIC_KEY_DIR with @ref PUBLIC_KEY_FILENAME.

    @param path: The path to the public key.

    @return The public key or None when there is an error opening the public key file.
    """
    if not path:
        path = f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}"
    with open(path, "rb") as file:
        return file.read()
    return None


def check_if_directory_contains_keys(device_path: str) -> bool:
    """!
    Check if the device_path contains the private key and the @ref PUBLIC_KEY_DIR contains the public key with @ref PUBLIC_KEY_FILENAME.

    @param device_path: The path to the device.

    @return True if both files exist, False otherwise.
    """
    return os.path.exists(
        f"{device_path}/{PRIVATE_KEY_DIR}{PRIVATE_KEY_FILENAME}{ENCRYPTED_EXTENSION}"
    ) and os.path.exists(f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}")
