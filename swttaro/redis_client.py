import redis

conf = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 1,
    'password': '',
    'socket_timeout': None,
    'encoding': 'utf-8'
}
connection_pool = redis.ConnectionPool(**conf)
# connection_pool = redis.ConnectionPool.from_url('redis://[:password]@host:port/db')


def get_redis_client():
    client = redis.Redis(connection_pool=connection_pool)

    return client


def get_connection_pool_info():
    info = {
        # '_available_connections': connection_pool._available_connections,
        '_created_connections': connection_pool._created_connections,
        '_in_use_connections': connection_pool._in_use_connections,
    }
    return info


def init_min_connections(count=0):
    # 每预生成一个连接大约需要用时2s
    if count >= connection_pool._created_connections:
        while count:
            count -= 1
            connection = connection_pool.make_connection()
            connection_pool._in_use_connections.add(connection)
            try:
                connection.connect()
            except Exception:
                connection_pool.release(connection)
                raise


init_min_connections(count=1)


class RedisBase:

    def __init__(self):
        self._client = get_redis_client()

    @property
    def pool_info(self):
        return get_connection_pool_info()

    def delete(self, key):
        return self._client.delete(key)

    def exists(self, key):
        return self._client.exists(key)

    def keys(self, pattern=''):
        return self._client.keys(pattern)


class StringRedis(RedisBase):

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        ex: 过期时间（秒）
        px: 过期时间（毫秒）
        nx: 如果设置为True: 则只有name不存在时: 当前set操作才执行
        xx: 如果设置为True: 则只有name存在时: 当前set操作才执行
        """
        self._client.set(name, value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, name, default=None):
        value = self._client.get(name)
        if value is None:
            return default

        return str(value, encoding='utf-8')


class NumberRedis(RedisBase):

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        ex: 过期时间（秒）
        px: 过期时间（毫秒）
        nx: 如果设置为True: 则只有name不存在时: 当前set操作才执行
        xx: 如果设置为True: 则只有name存在时: 当前set操作才执行
        """
        self._client.set(name, int(value), ex=ex, px=px, nx=nx, xx=xx)

    def get(self, name, default=None):
        value = self._client.get(name)
        if value is None:
            return default

        return int(value)

    def incr(self, name, amount=1):
        self._client.incr(name, amount)

    def decr(self, name, amount=1):
        self._client.decr(name, amount)


class HashRedis(RedisBase):

    def hset(self, name, key, value):
        self._client.hset(name, key, value)

    def hget(self, name, key, default=None):
        value = self._client.hget(name, key)
        if value is None:
            return default

        return str(value, encoding='utf-8')

    def hdel(self, name, key):
        self._client.hdel(name, key)
