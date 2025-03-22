from Crypto.PublicKey import RSA
import Crypto.Hash.SHA256 as SHA256
from Crypto.Signature import pss

SIGNATURE_LENGTH = 512


def sign_pdf(file_path: str, private_key: bytes, signed_file_path=None):
    if signed_file_path is None:
        signed_file_path = file_path.replace(".pdf", "_signed.pdf")

    with open(file_path, "rb") as f:
        data = f.read()

    rsa_key = RSA.import_key(private_key)
    signature = pss.new(rsa_key).sign(SHA256.new(data))

    with open(signed_file_path, "wb") as f:
        f.write(data)
        f.write(signature)


def verify_pdf(file_path: str, public_key: bytes) -> bool:
    with open(file_path, "rb") as f:
        data = f.read()

    pdf_data = data[:-SIGNATURE_LENGTH]
    signature = data[-SIGNATURE_LENGTH:]

    rsa_key = RSA.import_key(public_key)
    pdf_hash = SHA256.new(pdf_data)
    verifier = pss.new(rsa_key)
    try:
        verifier.verify(pdf_hash, signature)
        return True
    except (ValueError, TypeError):
        return False
