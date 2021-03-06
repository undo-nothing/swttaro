import unittest

from swttaro import i18n


class I18NTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_i18_text(self):
        print(i18n.get_i18_text('test'))
        print(i18n.get_i18_text(['test', 'test1']))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(I18NTest('test_get_i18_text'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
