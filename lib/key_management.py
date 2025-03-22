import os

from lib.crypt import *

PRIVATE_KEY_DIR = ""
PRIVATE_KEY_FILENAME = "private_key.pem"
ENCRYPTED_EXTENSION = ".aes"
PUBLIC_KEY_DIR = os.getcwd()
PUBLIC_KEY_FILENAME = "public_key.pub"


def generate_and_save_keys(device_path: str, pin: str) -> tuple[str, str]:
    private_key, public_key = generate_rsa_key_pair()
    return (
        encrypt_and_save_private_key(pin, device_path, private_key),
        save_public_key(public_key),
    )


def encrypt_and_save_private_key(pin: str, device_path: str, private_key: bytes):
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


def save_public_key(public_key: bytes):
    public_key_path = f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}"
    with open(
        public_key_path,
        "wb",
    ) as file:
        file.write(public_key)
    return public_key_path


def read_and_decrypt_private_key(pin: str, device_path: str) -> bytes:
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
    if not path:
        path = f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}"
    with open(path, "rb") as file:
        return file.read()
    return None


def check_if_directory_contains_keys(device_path: str) -> bool:
    return os.path.exists(
        f"{device_path}/{PRIVATE_KEY_DIR}{PRIVATE_KEY_FILENAME}{ENCRYPTED_EXTENSION}"
    ) and os.path.exists(f"{PUBLIC_KEY_DIR}/{PUBLIC_KEY_FILENAME}")
