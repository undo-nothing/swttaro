import base64
from binascii import b2a_hex, a2b_hex

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.PublicKey import RSA

AES_PASSWORD = b'test#aespassword'
AES_IV = b'1111111111#aesiv'

random_generator = Random.new().read


def get_keys():
    rsa = RSA.generate(1024, random_generator)

    public_pem = rsa.publickey().exportKey()
    private_pem = rsa.exportKey()

    pub_key = public_pem.decode()
    pri_key = private_pem.decode()

    return pub_key, pri_key


PUBLIC_KEY, PRIVATE_KEY = get_keys()


def rsa_encrypt(source_data):
    if not isinstance(source_data, bytes):
        source_data = bytes(source_data, encoding='utf-8')

    rsa_key = RSA.importKey(PUBLIC_KEY)
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypt_data = base64.b64encode(cipher.encrypt(source_data))

    return str(encrypt_data, encoding='utf-8')


def rsa_decrypt(encrypt_data):
    if not isinstance(encrypt_data, bytes):
        encrypt_data = bytes(encrypt_data, encoding='utf-8')

    rsa_key = RSA.importKey(PRIVATE_KEY)
    cipher = PKCS1_v1_5.new(rsa_key)
    source_data = cipher.decrypt(
        base64.b64decode(encrypt_data), random_generator)

    return str(source_data, encoding='utf-8')


def filling_data(data, restore=False):
    if restore:
        return data[0:-ord(data[-1])]
    block_size = AES.block_size
    return data + (block_size - len(data) % block_size) * chr(block_size - len(data) % block_size)


def aes_encrypt(content):
    if isinstance(content, bytes):
        content = str(content, encoding='utf-8')
    cipher = AES.new(AES_PASSWORD, AES.MODE_CBC, AES_IV)
    encrypted = cipher.encrypt(filling_data(content).encode('utf-8'))
    result = b2a_hex(encrypted).decode('utf-8')
    return result


def aes_decrypt(content):
    if isinstance(content, str):
        content = content.encode('utf-8')
    cipher = AES.new(AES_PASSWORD, AES.MODE_CBC, AES_IV)
    result = cipher.decrypt(a2b_hex(content)).decode('utf-8')
    return filling_data(result, restore=True)

