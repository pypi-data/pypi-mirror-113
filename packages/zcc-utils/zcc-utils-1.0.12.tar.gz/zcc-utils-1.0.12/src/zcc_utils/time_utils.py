import datetime
import zcc_utils.math_utils as math_utils


def second_to_minute(second: int):
    """
    秒转分钟
    :param second: 秒 int
    :return: 分钟 float
    """
    return second / 60


def second_to_hour(second: int):
    """
    秒转小时
    :param second: 秒 int
    :return: 小时 float
    """
    return second / 60 / 60


def float_hour_to_time(hour: float):
    """
    float类型的小时转time类型，12.99小时=>12:59:24
    :param hour:
    :return:
    """
    minute = math_utils.get_after_point_number_to_float(hour) * 60
    second = math_utils.get_after_point_number_to_float(minute) * 60
    return datetime.time(hour=int(hour), minute=int(minute), second=int(second))

def standard_time_format(time:str)->str:
    """
    将字符串时间转换为标准格式，例如 2019-1-3 15:29:08-> 2019-01-03 15:29:08
    :param time: 非标准格式的时间字符串
    :return: 标准格式的时间字符串
    """
    return str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))



if __name__ == "__main__":
    # time_local = time.localtime(1620557507)
    # print(type(time_local))
    # print(time_local)
    print(float_hour_to_time(12.99))
