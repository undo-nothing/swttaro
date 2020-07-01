import unittest

from swttaro import i18n


class I18NTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_i18_text(self):
        i18n.get_i18_text('测试')
        i18n.get_i18_text(['测试', '测试1'])


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(I18NTest('test_get_i18_text'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
