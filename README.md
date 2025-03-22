# PAdES

Application that allows the user to sign a PDF file with a digital signature. It stores an encrypted version of the private key on the USB drive. 

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run

### Generate key pair:

```bash
python generate_signing_key.py
```

During the generation of the key pair, the user will be asked to enter a PIN. This PIN will be used to encrypt the private key and store it on the USB drive.

Public key will be stored in `public_key.pub` file.

### Sign a PDF file or verify a signature:

```bash
python pades.py
``` 

When signing a PDF file, the user will be asked to enter the PIN to decrypt the private key. Make sure the USB drive is connected to the computer.