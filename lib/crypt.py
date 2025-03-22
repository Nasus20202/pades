import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import Crypto.Cipher.AES as AES


def hash_string(string: str) -> str:
    return SHA256.new(string.encode("utf-8")).digest()


def generate_rsa_key_pair(key_size: int = 4096) -> tuple[str, str]:
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_data_with_aes(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, tag, ciphertext


def decrypt_data_with_aes(
    nonce: bytes, tag: bytes, ciphertext: bytes, key: bytes
) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def merge_cipher_data(nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    return nonce + tag + ciphertext


def split_cipher_data(data: bytes) -> tuple[bytes, bytes, bytes]:
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    return nonce, tag, ciphertext
