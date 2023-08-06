def get_after_point_number_to_str(number: float):
    """
    获取小数点后的数，1.2 => 2
    :param number: 数字 float
    :return: 小数点后的数字 string
    """
    s1_list = str(number).split('.')
    return s1_list[1]


def get_after_point_number_to_float(number: float):
    """
    获取小数点后的数，1.2=>0.2
    :param number: 数字 float
    :return: 小数点后的数字 float
    """
    s1_list = str(number).split('.')
    return float('0.{0}'.format(s1_list[1]))


if __name__ == "__main__":
    print(get_after_point_number_to_float(1.2))
