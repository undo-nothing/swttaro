import functools
import time


def time_it(method):
    """
    t_start - t_end = used_time

    you can offer a dict to store the timing result

    example:
    log_time_container = {}
    result = SomeClass.get_all_result(log_time=log_time_container)

    :param method: callable
    :return:
    """
    @functools.wraps(method)
    def timed(*args, **kw):
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            log_time = kw.pop('log_time')
            t_start = time.time()
            result = method(*args, **kw)
            t_end = time.time()
            kw['log_time'] = log_time
            kw['log_time'][name] = int((t_end - t_start) * 1000)
        else:
            t_start = time.time()
            result = method(*args, **kw)
            t_end = time.time()
            time_display = '--- {: >10.5f} ms --- {!r}'.format((t_end - t_start) * 1000, method.__name__)
            print("\n\033[32m", end='')
            print(time_display, end='\033[0m')
            print('')

        return result

    return timed
