from Crypto.PublicKey import RSA
import Crypto.Hash.SHA256 as SHA256
from Crypto.Signature import pss
from PyPDF2 import PdfReader, PdfWriter


def sign_pdf(file_path: str, private_key: bytes, signed_file_path=None):
    if signed_file_path is None:
        signed_file_path = file_path.replace(".pdf", "_signed.pdf")

    with open(file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        pdf_writer = PdfWriter()
        pdf_writer.append_pages_from_reader(pdf_reader)
        data = f.read()

    rsa_key = RSA.import_key(private_key)
    signature = pss.new(rsa_key).sign(SHA256.new(data))

    pdf_writer.add_metadata({"/Signature": signature.hex()})
    with open(signed_file_path, "wb") as f:
        pdf_writer.write(f)


def verify_pdf(file_path: str, public_key: bytes) -> bool:
    with open(file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        data = f.read()

    rsa_key = RSA.import_key(public_key)
    signature = pdf_reader.metadata.get("/Signature")
    if signature is None:
        return False

    return pss.new(rsa_key).verify(SHA256.new(data), signature)
