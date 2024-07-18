# KUDO: Decoder Toolkit

KUDO is a comprehensive decoder toolkit offers a variety of decoding algorithms to decrypt and decode different types of encoded data.

## Available Algorithms

1. Advanced Encryption Standard (AES)
2. ROT13
3. Rivest-Shamir-Adleman (RSA)
4. ASCII85
5. Base32
6. Base64
7. Caesar Cipher
8. Hexadecimal
9. HTML Entity
10. Morse Code
11. PunnyCode
12. Quoted Printable
13. Unicode
14. UNIX Datetime
15. URL
16. Vigenere Cipher
17. XOR
18. Brainfuck
19. Reversed Word
20. Affine Cipher
21. Base58


## Usage

To use KUDO, simply run the script and follow the on-screen prompts to decode your encoded data. Each algorithm has its own specific requirements and input format.

```python
# Example usage for AES decryption
key = "your_aes_key_here"
ciphertext_b64 = "your_base64_encoded_ciphertext_here"
plaintext = decrypt_aes(key.encode('utf-8'), base64.b64decode(ciphertext_b64))
print("Decrypted plaintext:", plaintext)
```

Here's a README.md for your tool:

markdown

# KUDO: Decoder Toolkit

KUDO is a comprehensive decoder toolkit inspired by the brilliant cryptanalyst Conan from Detective Conan. This tool offers a variety of decoding algorithms to decrypt and decode different types of encoded data.

![KUDO](kudo_image.png) <!-- Insert your kudo ASCII art as an image here -->

## Author

- **Veilwr4ith**

## Description

KUDO is designed to assist in the decoding and decryption of various encoding schemes and cryptographic algorithms. The toolkit includes support for numerous algorithms, making it a versatile tool for anyone working with encoded data.

## Available Algorithms

1. Advanced Encryption Standard (AES)
2. ROT13
3. Rivest-Shamir-Adleman (RSA)
4. ASCII85
5. Base32
6. Base64
7. Caesar Cipher
8. Hexadecimal
9. HTML Entity
10. Morse Code
11. PunnyCode
12. Quoted Printable
13. Unicode
14. UNIX Datetime
15. URL
16. Vigenere Cipher
17. XOR
18. Brainfuck
19. Reversed Word
20. Affine Cipher
21. Base58

## Usage

To use KUDO, simply run the script and follow the on-screen prompts to decode your encoded data. Each algorithm has its own specific requirements and input format.

```python
# Example usage for AES decryption
key = "your_aes_key_here"
ciphertext_b64 = "your_base64_encoded_ciphertext_here"
plaintext = decrypt_aes(key.encode('utf-8'), base64.b64decode(ciphertext_b64))
print("Decrypted plaintext:", plaintext)
```

## Installation

KUDO requires Python 3 and the following packages:

- pycryptodome
- base64
- base58
- idna
- quopri

```bash
pip install pycryptodome base58 idna quopri
```

```bash
python3 kudo.py
```

## Author

- **Veilwr4ith**

