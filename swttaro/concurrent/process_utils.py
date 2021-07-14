import time
import multiprocessing 


def process_run(fn, arg_list=None, kwarg_list=None, pool_size=10, callback=None, return_result=None):
    '''
    进程运行过程不允许ctrl-c中断
    '''
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

    with multiprocessing.Pool(pool_size) as pool:
        handle_list = []
        for arg, kwarg in zip(arg_list, kwarg_list):
            task = pool.apply_async(fn, arg, kwarg, callback=callback)
            handle_list.append(task)

        return [i.get() for i in handle_list] if return_result else handle_list


def result_callback(result):
    print('result callback:', result)
    return result


def test_target(*arg, **kwarg):
    print('>>>>>>', arg, kwarg)
    time.sleep(int(arg[0]))
    return arg, kwarg


def test():
    process_run(test_target,
               [['2', 'test1'], ['4', 'cc1']],
               [{'aa': 'bb'}, {'cc': 'dd'}],
               pool_size=5,
               callback=result_callback,
               return_result=True)


if "__main__" == __name__:
    test()
