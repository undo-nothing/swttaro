import unittest

from swttaro import debug_tools


@debug_tools.time_it
def some_func():
    pass


class DebugToolsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basecolor(self):
        some_func()
        log_time = {}
        some_func(log_time=log_time)
        print(log_time)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(DebugToolsTest('test_basecolor'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
