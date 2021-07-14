import asyncio

from asyncio_pool import AioPool


async def _callback(result, err, callback, *arg, **kwarg):
    return callback(result, err)


async def _asyncio_run(fn, arg_list=None, kwarg_list=None, pool_size=10, callback=None, return_result=True):
    arg_count = len(arg_list) if arg_list else 0
    kwarg_count = len(kwarg_list) if kwarg_list else 0
    params_count = max(arg_count, kwarg_count)
    pool_size = min(params_count, pool_size)
    if not arg_list:
        arg_list = [[] for i in range(params_count)]
    if not kwarg_list:
        kwarg_list = [{} for i in range(params_count)]

    if len(kwarg_list) != len(arg_list):
        raise Exception('len(arg):%s != len(kwarg):%s' %
                        (len(arg_list), len(kwarg_list)))

    futures = []
    async with AioPool(size=pool_size) as pool:
        for arg, kwarg in zip(arg_list, kwarg_list):
            task = fn(*arg, **kwarg)
            if callback:
                fut = await pool.spawn(task, cb=_callback, ctx=callback)
            else:
                fut = await pool.spawn(task)
            futures.append(fut)

    return [i.result() for i in futures] if return_result else futures


def asyncio_run(fn, arg_list=None, kwarg_list=None, pool_size=10, callback=None, return_result=True):
    '''
    协程运行过程允许ctrl-c中断
    '''
    loop = asyncio.get_event_loop()
    task = _asyncio_run(fn, arg_list=arg_list, kwarg_list=kwarg_list,
                        pool_size=pool_size, callback=callback, return_result=return_result)
    return loop.run_until_complete(task)


def result_callback(result, err):
    print('result callback: %s' % result)
    return result


async def do_some_work(*arg, **kwarg):
    x = arg[0]
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


async def open_url(url, params={}):
    import aiohttp
    jwt_token  = '11'
    headers = {
        'User-Agent': "Mozilla/5.0 ",
        "Content-Type": "application/json",
        "Authorization": "JWT %s" % jwt_token,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, headers=headers) as response:
            result = await response.text()
            print(result)
        return result


def test():
    urls = [['http://192.168.218.24:6883/drf-docs/'] for i in range(300)]
    asyncio_run(open_url, urls, pool_size=1)


if "__main__" == __name__:
    test()
