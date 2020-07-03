import datetime
import fnmatch

offset = datetime.datetime.fromtimestamp(0) - datetime.datetime.utcfromtimestamp(0)


def is_fnmatch(file_path, fnmatch_list):
    for key in fnmatch_list:
        if fnmatch.fnmatch(file_path, key):
            return True
    return False


def utc_to_local(utc_time, time_format="%Y-%m-%d %H:%M:%S"):
    if isinstance(utc_time, datetime.datetime):
        return utc_time + offset
    else:
        return datetime.datetime.strptime(utc_time, time_format) + offset
