
import hashlib
import urllib
from urllib.parse import urlparse
from urllib.request import unquote
from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode

VERSION = '0.1.11'
appKey = '434a209a5ce141c3b726de067835d7f0'
signKey = 'xhdiwjnchekd4d512chdjx5d8e4c394D2D7S'

class security:

    def __init__(self):
        self.appKey = appKey
        self.signKey = signKey
        self.blockSize = 16
        self.encKey = self.enc_key()
        self.dynamicKey = self.dynamic_key()
         

    def aes_decrypt(self, raw):
        cipher = AES.new(self.encKey, AES.MODE_ECB)
        decrypted = cipher.decrypt(bytes(raw))

        # Remove the padding
        decrypted = self._unpad(decrypted)   

        return decrypted

    def aes_encrypt(self, raw):
        # Make sure to pad the data
        self._pad(raw)
        
        cipher = AES.new(self.encKey, AES.MODE_ECB)
        encrypted = cipher.encrypt(bytes(raw))
            
        return encrypted

    def _pad(self, s):
        pad = self.blockSize - (len(s) % self.blockSize)
        s.extend([pad] * pad)
       
    def _unpad(self, s):
        return s[:-s[-1]]

    def enc_key(self):
        m = hashlib.md5()
        # Hash the signKey
        m.update(self.signKey.encode('ascii'))
        # Use the HEX output of the hash
        key = bytes.fromhex(m.hexdigest())
        return key

    def dynamic_key(self):
        m = hashlib.md5()
        # Hash the appKey
        m.update(self.appKey.encode('ascii'))
        # Use only half the HEX output of the hash
        key = bytes.fromhex(m.hexdigest()[:16])
        return key

    def encode32_data(self, raw):
        combine = raw + signKey.encode()
        m = hashlib.md5()
        m.update(combine)
        key = bytes.fromhex(m.hexdigest())
        return key
