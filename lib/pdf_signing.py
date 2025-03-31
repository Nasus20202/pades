## @file pdf_signing.py
# This module contains functions related to signing and verifying signed PDF files.

from Crypto.PublicKey import RSA
import Crypto.Hash.SHA256 as SHA256
from Crypto.Signature import pss

## @var SIGNATURE_LENGTH
# The length of the signature in bytes.
SIGNATURE_LENGTH = 512


def sign_pdf(file_path: str, private_key: bytes, signed_file_path=None) -> None:
    """!
    Sign a PDF file with a private key and save it to the signed_file_path.

    The signature is constructed by hashing the PDF file and then signing the hash with the provided private key.
    This signed hash is then appended to the end of the file.

    @param file_path: The path to the PDF file to sign.
    @param private_key: The private key to sign the PDF file with.
    @param signed_file_path: The path to save the signed PDF file to.
    If None, the file will be saved in the same directory with the same name but with "_signed" suffix.

    @return None
    """
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
    """!
    Verify the signature of a signed PDF file.

    The signature is verified by hashing the PDF contents (excluding embedded signature) and then comparing the hash
    to the signature extracted from the file (the signature is first decrypted with the public key).

    @param file_path: The path to the signed PDF file to verify.
    @param public_key: The public key used to verify the signature.

    @return True if the signature is valid, False otherwise.
    """
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
