import unittest

from swttaro import xlrd_utils


class XlrdUtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict_reader(self):
        with open(r'../data/xlrd_example.xls', 'rb') as f:
            xlrd_reader = xlrd_utils.DictReader(f)
            for data in xlrd_reader:
                print(data)

    def test_reader(self):
        with open(r'../data/xlrd_example.xls', 'rb') as f:
            xlrd_reader = xlrd_utils.Reader(f)
            for data in xlrd_reader:
                print(data)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(XlrdUtilsTest('test_dict_reader'))
    suite.addTest(XlrdUtilsTest('test_reader'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
