import json
import os
from base64 import b64decode, b64encode
from Crypto.Cipher import AES

key = str.encode(os.environ.get('ENCRYPTION_KEY'))

def encrypt(b64data):
    data = str.encode(b64data)
    header = b"ResetPasswordRequest"
    print(type(header))
    print(type(data))

    cipher = AES.new(key, AES.MODE_EAX)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag) ]
    result = json.dumps(dict(zip(json_k, json_v)))
    return b64encode(str.encode(result))


def decrypt(b64data):
    data = b64decode(b64data)
    b64 = json.loads(data)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in json_k}

    cipher = AES.new(key, AES.MODE_EAX, nonce=jv['nonce'])
    cipher.update(jv['header'])
    plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    return plaintext.decode('utf-8')