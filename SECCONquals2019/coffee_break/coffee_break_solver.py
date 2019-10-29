import sys
from Crypto.Cipher import AES
import base64


def encrypt(key, text):
    s = ''
    for i in range(len(text)):
        s += chr((((ord(text[i]) - 0x20) + (ord(key[i % len(key)]) - 0x20)) % (0x7e - 0x20 + 1)) + 0x20)
    return s


# I tried bruteforcing!!!!!!!!
def decrypt(key, enc_answer):
    plaintext = ''
    for i in range(len(enc_answer)):
        for j in range(0x20, 0x7f):
            enc_challenge_i = encrypt(key, plaintext + chr(j))[-1]
            if enc_answer[i] == enc_challenge_i[-1]:
                plaintext += chr(j)
                break
    return plaintext


def main():
    ciphertext = "FyRyZNBO2MG6ncd3hEkC/yeYKUseI/CxYoZiIeV2fe/Jmtwx+WbWmU1gtMX9m905"

    key1 = "SECCON"
    key2 = "seccon2019"

    dec_1 = base64.b64decode(ciphertext)
    cipher = AES.new((key2 + chr(0x00) * (16 - (len(key2) % 16))).encode(), AES.MODE_ECB)
    dec_2 = cipher.decrypt(dec_1)
    dec_2_notpadded = dec_2[:-5]
    dec_3 = decrypt(key1, dec_2_notpadded.decode())
    print(dec_3)
    input("[END OF PROGRAM]")

if __name__ == '__main__':
    main()