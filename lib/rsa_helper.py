# -*- coding:utf-8 -*-
import os
import base64
import rsa


class RsaHelper():

    def __init__(self, bit_size, pool_size=8):
        self.bit_size = bit_size
        self.pool_size = pool_size

    # 接收字符串 返回bs64后的字符串
    def encrypt(self, str, pub):
        str_bytes = str.encode('utf-8')
        crypto = rsa.encrypt(str_bytes, pub)
        bs64 = base64.b64encode(crypto)
        return bs64

    # 接收来自bs64后的字符串 返回解密的字符串
    def decrypt(self, str, priv):
        data = base64.b64decode(str)
        result = rsa.decrypt(data, priv)
        return result.decode('utf-8')

    def generate_key(self):
        (pub, priv) = rsa.newkeys(self.bit_size, poolsize=self.pool_size)
        return (pub, priv)

    def store_to_file(self, file, key_data):
        if os.path.exists(file) is False:
            return False
        if os.access(file, os.R_OK) is False:
            return False
        file_handle = open(file, mode='wb+')
        file_handle.write(key_data.save_pkcs1())
        return True

    def key_from_file(self, file, flag):
        key = None
        if os.path.exists(file) is False:
            return key
        if os.access(file, os.R_OK) is False:
            return key

        # 公钥
        if flag == 'public':
            with open(file, mode='rb') as publicfile:
                data = publicfile.read()
                try:
                    key = rsa.PublicKey.load_pkcs1(data)
                except:
                    key = rsa.PublicKey.load_pkcs1_openssl_pem(data)
        # 私钥
        else:
            with open(file, mode='rb') as privfile:
                data = privfile.read()
                key = rsa.PrivateKey.load_pkcs1(data)
        return key

    # 生成签名
    def sign(self, message, privvate_key, hash):
        return rsa.sign(message.encode('utf-8'), privvate_key, hash)

    # 验证签名
    def verify(self, message, signature, pub_key):
        return rsa.verify(message.encode('utf-8'), signature, pub_key)
