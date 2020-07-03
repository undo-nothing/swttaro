import os
import unittest

from swttaro.crypto_utils import aes_decrypt, aes_encrypt, rsa_decrypt, rsa_encrypt


class CryptoUtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_aes(self):
        in_list = ['1234', b'1234', '5678', b'5678']
        for i in in_list:
            aes_decrypt(aes_encrypt(i))

    def test_rsa(self):
        in_list = ['1234', b'1234', '5678', b'5678']
        for i in in_list:
            rsa_decrypt(rsa_encrypt(i))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CryptoUtilsTest('test_aes'))
    suite.addTest(CryptoUtilsTest('test_rsa'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
