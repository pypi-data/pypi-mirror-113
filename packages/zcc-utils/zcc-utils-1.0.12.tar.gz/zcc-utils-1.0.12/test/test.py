import requests
from typing import List
from src.zcc_utils import time_utils


if __name__ == "__main__":
    # time_local = time.localtime(1620557507)
    # print(type(time_local))
    # print(time_local)
    # print(time_utils.float_hour_to_time(12.99))

    str_p = '2019-1-3 15:29:08'

    dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')

    print(dateTime_p,type(dateTime_p))  # 2019-01-30 15:29:08
    print(str(dateTime_p),type(str(dateTime_p)))  # 2019-01-30 15:29:08