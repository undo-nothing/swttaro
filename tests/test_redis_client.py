import unittest

from swttaro import redis_client


class RedisClientUtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_string_redis(self):
        sr = redis_client.StringRedis()
        sr.set('testtt', 'aaaaaaaaaa')
        a = sr.get('testtt')
        b = sr.get('testtt111111', 'bbbbbbbb')
        print(a, b)

    def test_number_redis(self):
        sr = redis_client.NumberRedis()
        sr.set('test123', '123')
        a = sr.get('test123')
        print(a, type(a))
        sr.incr('test123')
        print(sr.get('test123'))
        sr.decr('test123')
        print(sr.get('test123'))



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(RedisClientUtilsTest('test_string_redis'))
    suite.addTest(RedisClientUtilsTest('test_number_redis'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
