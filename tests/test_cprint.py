import os
import unittest

from swttaro import cprint


class CprintTest(unittest.TestCase):

    def setUp(self):
        print('Current terminal type: %s' % os.getenv('TERM'))
        pass

    def tearDown(self):
        pass

    def test_basecolor(self):
        print('Test basic colors:')
        cprint.grey('Grey color')
        cprint.red('Red color')
        cprint.green('Green color')
        cprint.yellow('Yellow color')
        cprint.blue('Blue color')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CprintTest('test_basecolor'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
