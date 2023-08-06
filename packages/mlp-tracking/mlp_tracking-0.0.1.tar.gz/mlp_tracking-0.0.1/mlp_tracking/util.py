import time


def get_current_time(TIME_FORMAT="%Y-%m-%d %H:%M:%S"):
    return time.strftime(TIME_FORMAT, time.localtime())
