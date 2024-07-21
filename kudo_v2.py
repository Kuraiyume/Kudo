"""
------------------------------------------
KUDO: Decoder Toolkit                    |
                                         |
Author: Veilwr4ith                       |
------------------------------------------
"""

import os
import base64
import base58
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import html
import idna
import quopri
import datetime
import urllib.parse
import argparse

# banner

kudo = """			          .-""-.
 /$$   /$$                 /$$   / .--. \\
| $$  /$$/                | $$  / /    \\ \\
| $$ /$$/  /$$   /$$  /$$$$$$$  | |.-""-.|  
| $$$$$/  | $$  | $$ /$$__  $$ ///`.::::.`\\
| $$  $$  | $$  | $$| $$  | $$||| ::/  \:: ; 
| $$\\  $$ | $$  | $$| $$  | $$||; ::\__/:: ; 
| $$ \\  $$|  $$$$$$/|  $$$$$$$ \\\\\\ '::::' / 
|__/  \\__/ \\______/  \\_______/  `=':-..-'`

No matter how clever the code, there's always a way to break it.
"""
# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.',
    ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# NATO Dictionary
NATO_DICT = {
    "ALPHA": "A", "BRAVO": "B", "CHARLIE": "C", "DELTA": "D",
    "ECHO": "E", "FOXTROT": "F", "GOLF": "G", "HOTEL": "H",
    "INDIA": "I", "JULIETT": "J", "KILO": "K", "LIMA": "L",
    "MIKE": "M", "NOVEMBER": "N", "OSCAR": "O", "PAPA": "P",
    "QUEBEC": "Q", "ROMEO": "R", "SIERRA": "S", "TANGO": "T",
    "UNIFORM": "U", "VICTOR": "V", "WHISKEY": "W", "XRAY": "X",
    "YANKEE": "Y", "ZULU": "Z"
}

# Help Menu
help_menu = """
Available Algorithms:
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
22. A1Z26
23. Rail Fence Cipher
24. Substitution Cipher
25. Tap Code
26. Nihilist Cipher
27. Polybius Cipher
28. NATO Phonetics
"""

"""Function for decrypting AES Encryption"""
def decrypt_aes(key, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv=ciphertext[:AES.block_size])
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    pad_length = plaintext[-1]
    plaintext = plaintext[:-pad_length]
    return plaintext.decode('utf-8')

"""Function for decoding ROT13 Algorithm"""
def rot13_decoder(text):
    decoded_text = ""
    for char in text:
        if 'A' <= char <= 'Z':
            decoded_text += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            decoded_text += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        else:
            decoded_text += char
    return decoded_text

"""Function for decrypting RSA Encryption"""
def decrypt_rsa(private_key_path, ciphertext_b64):
    with open(private_key_path, 'r') as f:
        private_key = f.read()
    try:
        private_key = RSA.import_key(private_key)
    except ValueError as e:
        raise ValueError("Invalid RSA private key format") from e
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    plaintext = cipher_rsa.decrypt(ciphertext)
    return plaintext.decode('utf-8')

"""Function for decoding ASCII85 Algorithm"""
def decode_ascii85(encoded_data):
    try:
        decoded_data = base64.a85decode(encoded_data.encode('ascii'))
        return decoded_data.decode('utf-8')
    except base64.binascii.Error:
        return "Error: Invalid ASCII85 encoded data"

"""Function for decoding Base32 Algorithm"""
def base32_decode(encoded_text):
    try:
        decoded_bytes = base64.b32decode(encoded_text)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text
    except:
        return "Decoding Failed."

"""Function for decoding Base64 Algorithm"""
def base64_decode(encoded_text):
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text
    except:
        return "Decoding Failed."

"""Function for decoding Caesar Cipher"""
def caesar_decoder(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                decrypted_text += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
        else:
            decrypted_text += char
    return decrypted_text

"""Function for decoding Hexadecimal"""
def hex_to_plaintext(hex_string):
    try:
        hex_string = hex_string.replace(" ", "")
        byte_data = bytes.fromhex(hex_string)
        plaintext = byte_data.decode('utf-8')
        return plaintext
    except Exception as i:
        print("Error:", i)
        return None
    
"""Function for decoding HTML Entity"""
def html_entity_decoder(text):
    decoded_text = html.unescape(text)
    return decoded_text

"""Function for decoding Morse Code"""
def morse_decoder(text):
    words = text.split('/')
    decoded_message = []
    for word in words:
        letters = word.split()
        decoded_word = ''
        for letter in letters:
            decoded_word += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(letter)]
        decoded_message.append(decoded_word)
    return ' '.join(decoded_message)

"""Function for decoding Punnycode"""
def punnycode_decoder(text):
    try:
        decoded_text = idna.decode(text)
        return decoded_text
    except idna.IDNAError as e:
        print(f"Error: {e}")
        return None
    
"""Function for decoding Quoted Printable"""
def quoted_printable_decoder(text):
    try:
        decoded_text = quopri.decodestring(text).decode('utf-8')
        return decoded_text
    except Exception as fuck:
        print("Error: ", fuck)

"""Function for decoding Unicode"""
def unicode_decoder(text):
    try:
        decoded_text = text.encode('utf-8').decode('unicode-escape')
        return decoded_text
    except UnicodeDecodeError:
        return "Error: Unable to decode Unicode text"
    
"""Function for decoding UnixTime"""
def unix_time_decoder(timestamp):
    try:
        timestamp = int(timestamp)
        date_time = datetime.datetime.utcfromtimestamp(timestamp)
        return date_time.strftime('%Y-%m-%d %H:%M:%S UTC')
    except ValueError:
        return "Invalid Unix timestamp"
    
"""Function for decoding URL"""
def url_decoder(encoded_urls):
    urls = encoded_urls.split(',')
    decoded_urls = []
    for encoded_url in urls:
        try:
            decoded_url = urllib.parse.unquote(encoded_url)
            decoded_urls.append(decoded_url)
        except Exception as e:
            return f"Error decoded URL '{encoded_url.strip()}': {e}"
    return '\n'.join(decoded_urls)

"""Function for decoding Vigenere Cipher"""
def vigenere_decode(ciphertext, keyword):
    keyword = keyword.upper()
    plaintext = ""
    keyword_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
            if char.islower():
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext += decrypted_char
            keyword_index += 1
        else:
            plaintext += char
    return plaintext

"""Function for decoding XOR"""
def xor_decode(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        plaintext += chr(ord(char) ^ key)
    return plaintext

"""Function for decoding Brainfuck"""
def brainfuck_decode(code):
    code = ''.join(filter(lambda x: x in ('+', '-', '<', '>', '[', ']', '.', ','), code))
    code_ptr = 0
    memory = [0]
    mem_ptr = 0
    output = ""
    loop_stack = []

    while code_ptr < len(code):
        command = code[code_ptr]

        if command == '>':
            mem_ptr += 1
            if mem_ptr == len(memory):
                memory.append(0)
        elif command == '<':
            mem_ptr = max(0, mem_ptr - 1)
        elif command == '+':
            memory[mem_ptr] = (memory[mem_ptr] + 1) % 256
        elif command == '-':
            memory[mem_ptr] = (memory[mem_ptr] - 1) % 256
        elif command == '.':
            output += chr(memory[mem_ptr])
        elif command == ',':
            pass  # Input is not supported
        elif command == '[':
            if memory[mem_ptr] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    code_ptr += 1
                    if code[code_ptr] == '[':
                        open_brackets += 1
                    elif code[code_ptr] == ']':
                        open_brackets -= 1
            else:
                loop_stack.append(code_ptr)
        elif command == ']':
            if memory[mem_ptr] != 0:
                code_ptr = loop_stack[-1]
            else:
                loop_stack.pop()

        code_ptr += 1

    return output

"""Function for decoding Reversed Words"""
def reversed_word_decoder(text):
    words = text.split()
    reversed_text = ' '.join(word[::-1] for word in words)
    return reversed_text

"""Function for decoding Affine Cipher"""
def affine_decoder(text, a, b):
    mod_inverse_a = pow(a, -1, 26)
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                decrypted_char = chr((mod_inverse_a * ((ord(char) - ord('A') - b) % 26)) + ord('A'))
            else:
                decrypted_char = chr((mod_inverse_a * ((ord(char) - ord('a') - b) % 26)) + ord('a'))
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

"""Function for decoding Base58"""
def base58_decode(encoded_text):
    decoded_bytes = base58.b58decode(encoded_text)
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text
"""Function for decoding A1Z26"""
def a1z26_decode(text):
    numbers = text.split()
    decoded_text = ''
    for number in numbers:
        if number.isdigit():
            decoded_text += chr(int(number) + 64)
        else:
            decoded_text += number
    return decoded_text

"""Function for decoding Rail Fence Cipher"""
def rail_fence_decoder(ciphertext, num_rails):
    if num_rails == 1:
        return ciphertext

    rail = [''] * num_rails
    direction = None
    row = 0
    for char in ciphertext:
        if row == 0:
            direction = 1
        elif row == num_rails - 1:
            direction = -1

        rail[row] += char
        row += direction

    result = ''.join(rail)
    return result

"""Function for decoding Substitution Cipher"""
def substitution_cipher_decoder(text, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = key.upper()
    decrypted_text = ''
    for char in text:
        if char.upper() in key:
            decrypted_char = alphabet[key.index(char.upper())]
            if char.islower():
                decrypted_char = decrypted_char.lower()
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

"""Function for decoding Tap Code"""
def tap_code_decoder(encoded_text):
    tap_code_dict = {
        '11': 'A', '12': 'B', '13': 'C', '14': 'D', '15': 'E',
        '21': 'F', '22': 'G', '23': 'H', '24': 'I', '25': 'J',
        '31': 'L', '32': 'M', '33': 'N', '34': 'O', '35': 'P',
        '41': 'Q', '42': 'R', '43': 'S', '44': 'T', '45': 'U',
        '51': 'V', '52': 'W', '53': 'X', '54': 'Y', '55': 'Z',
        '23': 'K'
    }
    pairs = encoded_text.split(' ')
    decoded_text = ''
    for pair in pairs:
        if pair in tap_code_dict:
            decoded_text += tap_code_dict[pair]
        else:
            decoded_text += pair
    return decoded_text

"""Function for decoding Nihilist Cipher"""
def nihilist_cipher_decoder(ciphertext, key):
    key_numbers = [ord(char.upper()) - 64 for char in key]
    ciphertext_numbers = [int(num) for num in ciphertext.split()]
    plaintext = ''
    key_index = 0

    for num in ciphertext_numbers:
        plain_num = num - key_numbers[key_index]
        if plain_num < 1:
            plain_num += 26
        plaintext += chr(plain_num + 64)
        key_index = (key_index + 1) % len(key_numbers)

    return plaintext

"""Function for decoding Polybius Cipher"""
def polybius_decoder(encoded_text):
    polybius_square = {
        '11': 'A', '12': 'B', '13': 'C', '14': 'D', '15': 'E',
        '21': 'F', '22': 'G', '23': 'H', '24': 'I', '25': 'K',
        '31': 'L', '32': 'M', '33': 'N', '34': 'O', '35': 'P',
        '41': 'Q', '42': 'R', '43': 'S', '44': 'T', '45': 'U',
        '51': 'V', '52': 'W', '53': 'X', '54': 'Y', '55': 'Z'
    }
    decoded_text = ""
    pairs = encoded_text.split()
    for pair in pairs:
        decoded_text += polybius_square.get(pair, "?")
    return decoded_text

"""Function for decoding NATO Phonetics"""
def nato_decoder(text):
    words = text.split()
    decoded_message = []
    for word in words:
        decoded_word = NATO_DICT.get(word.upper(), '')
        decoded_message.append(decoded_word)
    return ''.join(decoded_message)

def main():
    os.system("clear")
    print(kudo)
    parser = argparse.ArgumentParser(description="Decrypt various encoded/encoded texts.")
    parser.add_argument("-a", "--algo", help="Specify the algorithm to use for decoding", choices=[
        "rot13", "ascii85", "base32", "base64", "caesar", "hex", "html", "morse", "punnycode",
        "quoted_printable", "unicode", "unix_time", "url", "vigenere", "xor", "aes", "rsa",
        "brainfuck", "reversed_word", "affine", "base58", "a1z26", "railfence", "substitution",
        "tapcode", "nihilist", "polybius", "nato"], required=True)
    parser.add_argument("-d", "--data", help="Data to decrypt", required=True)
    parser.add_argument("-k", "--key", help="Key for decryption (if applicable)")
    parser.add_argument("-l", "--list_algo", action="store_true", help="List all available algorithms")

    args = parser.parse_args()

    if args.list_algo:
        print("Available algorithms:")
        for algo in [
            "rot13", "ascii85", "base32", "base64", "caesar", "hex", "html", "morse", "punnycode",
            "quoted_printable", "unicode", "unix_time", "url", "vigenere", "xor", "aes", "rsa",
            "brainfuck", "reversed_word", "affine", "base58", "a1z26", "railfence", "substitution",
            "tapcode", "nihilist", "polybius", "nato"]:
            print(f"  - {algo}")
        return

    algo = args.algo.lower()
    data = args.data

    if algo == "aes":
        # For AES, you need to provide a key and ciphertext
        key = input("Enter AES key: ")
        key_encode = key.encode('utf-8')
        ciphertext = base64.b64decode(data)
        print(decrypt_aes(key_encode, ciphertext))
    elif algo == "rot13":
        print(rot13_decoder(data))
    elif algo == "rsa":
        # For RSA, you need to provide a private key and ciphertext
        private_key = input("Enter RSA private key path: ")
        print(decrypt_rsa(private_key, data))
    elif algo == "ascii85":
        print(decode_ascii85(data))
    elif algo == "base32":
        print(base32_decode(data))
    elif algo == "base64":
        print(base64_decode(data))
    elif algo == "caesar":
        shift = int(input("Enter Caesar shift value: "))
        print(caesar_decoder(data, shift))
    elif algo == "hex":
        print(hex_to_plaintext(data))
    elif algo == "html":
        print(html_entity_decoder(data))
    elif algo == "morse":
        print(morse_decoder(data))
    elif algo == "punny":
        print(punnycode_decoder(data))
    elif algo == "quoted":
        print(quoted_printable_decoder(data))
    elif algo == "unicode":
        print(unicode_decoder(data))
    elif algo == "unixtime":
        print(unix_time_decoder(data))
    elif algo == "url":
        print(url_decoder(data))
    elif algo == "vigenere":
        keyword = input("Enter Vigenere keyword: ")
        print(vigenere_decode(data, keyword))
    elif algo == "xor":
        key = int(input("Enter XOR key: "))
        print(xor_decode(data, key))
    elif algo == "brainfuck":
        print(brainfuck_decode(data))
    elif algo == "reversed":
        print(reversed_word_decoder(data))
    elif algo == "affine":
        a = int(input("Enter Affine 'a' value: "))
        b = int(input("Enter Affine 'b' value: "))
        print(affine_decoder(data, a, b))
    elif algo == "base58":
        print(base58_decode(data))
    elif algo == "a1z26":
        print(a1z26_decode(data))
    elif algo == "railfence":
        num_rails = int(input("Enter number of rails: "))
        print(rail_fence_decoder(data, num_rails))
    elif algo == "substitution":
        key = input("Enter substitution key: ")
        print(substitution_cipher_decoder(data, key))
    elif algo == "tapcode":
        print(tap_code_decoder(data))
    elif algo == "nihilist":
        key = input("Enter Nihilist key: ")
        print(nihilist_cipher_decoder(data, key))
    elif algo == "polybius":
        print(polybius_decoder(data))
    elif algo == "nato":
        print(nato_decoder(data))
    else:
        print(f"Unsupported algorithm: {algo}")

if __name__ == "__main__":
    main()
