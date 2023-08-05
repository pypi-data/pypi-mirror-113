from . import ua_web_list
from . import ua_android_list
import random

ua_web_lists = ua_web_list.ua_web_list
ua_android_lists = ua_android_list.ua_android_list


def random_web_ua(num=1):
    # print("ua_web_lists",type(ua_web_lists))
    if num == 1:

        return random.choice(ua_web_lists)
    else:
        return random.sample(ua_web_lists, num)


def random_android_ua(num=1):
    # print("ua_android_lists",type(ua_android_lists))
    if num == 1:
        return random.choice(ua_android_lists)
    else:
        return random.sample(ua_android_lists, num)
