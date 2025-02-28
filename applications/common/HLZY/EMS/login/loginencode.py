from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


def encrypt_cfb(data, key):
    # 生成一个随机的初始化向量 (IV)
    iv = get_random_bytes(AES.block_size)

    # 创建 AES CFB 模式的 Cipher 对象
    cipher = AES.new(key, AES.MODE_CFB, iv)

    # 加密数据
    ciphertext = cipher.encrypt(data)

    # 将 IV 和密文一起返回，以便解密时使用
    return base64.b64encode(iv + ciphertext).decode('utf-8')


# 密钥
key = b'nebuveilnebuveil'

# 要加密的数据
data = b'IK*R^aNQE0'

# 调用加密函数
encrypted_data = encrypt_cfb(data, key)

print(f'Encrypted data: {encrypted_data}')
