# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/11
Description: <Brief description of the file>
"""
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 默认密钥
DEFAULT_KEY = b'nebuveilnebuveil'

def aes_encrypt(src, key_word=DEFAULT_KEY):
    key = key_word
    iv = key
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted = cipher.encrypt(pad(src.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')

def aes_decrypt(result, key_word=DEFAULT_KEY):
    key = key_word
    iv = key
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted = unpad(cipher.decrypt(base64.b64decode(result)), AES.block_size)
    return decrypted.decode('utf-8')

def base64_encrypt(src):
    encoded_word = src.encode('utf-8')
    return base64.b64encode(encoded_word).decode('utf-8')

# 示例用法
if __name__ == "__main__":
    plaintext = "IK*R^aNQE0"
    key = b'nebuveilnebuveil'  # 16字节的密钥

    # AES 加密
    encrypted_text = aes_encrypt(plaintext, key)
    print(f"Encrypted: {encrypted_text}")

    # AES 解密
    decrypted_text = aes_decrypt(encrypted_text, key)
    print(f"Decrypted: {decrypted_text}")

    # Base64 加密
    base64_encoded = base64_encrypt(plaintext)
    print(f"Base64 Encoded: {base64_encoded}")
