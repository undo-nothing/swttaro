import os

import unittest

from swttaro.search_str import SearchStr


class SearchStrTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search_str(self):
        ss = SearchStr()
        print(ss.search_str('search_str', os.path.abspath(__file__), match_all=True))

    def test_re_search_str(self):
        ss = SearchStr()
        print(ss.re_search_str(r'search_str', os.path.abspath(__file__), match_all=True))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SearchStrTest('test_search_str'))
    suite.addTest(SearchStrTest('test_re_search_str'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
