#!/usr/bin/env python

from Crypto.Cipher import AES
import os
import math

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))


def to_bytes(n):
    s = hex(n)
    s_n = s[2:]
    if 'L' in s_n:
        s_n = s_n.replace('L', '')
    if len(s_n) % 2 != 0:
        s_n = '0' + s_n
    decoded = s_n.decode('hex')

    pad = (len(decoded) % BLOCK_SIZE)
    if pad != 0: 
        decoded = "\0" * (BLOCK_SIZE - pad) + decoded
    return decoded


def remove_line(s):
    # returns the header line, and the rest of the file
    return s[:s.index(b'\n') + 1], s[s.index(b'\n')+1:]


def parse_header_ppm(f):
    data = f.read()

    header = ""

    for i in range(3):
        header_i, data = remove_line(data)
        header += header_i.decode()

    return header, data
        

def pad(pt):
    padding = BLOCK_SIZE - len(pt) % BLOCK_SIZE
    return pt + (chr(padding) * padding)


def aes_abc_decrypt(pt):
    # initialize encrypted_blocks
    c_blocks = [pt[i * BLOCK_SIZE : (i+1) * BLOCK_SIZE] for i in range(len(pt) // BLOCK_SIZE)]
    iv = c_blocks[0]
    
    # initialize plaintext_blocks
    p_blocks = []
    for i in range(len(c_blocks) - 1):
        prev_c_blk = int.from_bytes(c_blocks[i], 'big')
        curr_c_blk = int.from_bytes(c_blocks[i + 1], 'big')

        # encryption : c_blocks[i+1] = c_blocks[i] + p_blocks[i+1] mod UMAX
        # decryption : p_blocks[i+1] = c_blocks[i+1] - c_blocks[i] mod UMAX
        # where c_blocks[0] = p_blocks[0] = iv
        curr_p_blk = (curr_c_blk - prev_c_blk) % UMAX

        # decrypt AES_EBC using the KEY that can get from the result of previous decryption
        # this process may be optional in this problem
        curr_p_blk ^= 0x806de6300d62b81291a3dbc595e3140b

        p_blocks.append(curr_p_blk.to_bytes(16, 'big'))

    ct_abc = b"".join(p_blocks)
 
    return iv, ct_abc, pt


if __name__=="__main__":
    with open('body.enc.ppm', 'rb') as f:
        header, data = parse_header_ppm(f)
    
    iv, c_img, pt = aes_abc_decrypt(data)

    with open('decrypted.ppm', 'wb') as fw:
        fw.write(header.encode())
        fw.write(c_img)
