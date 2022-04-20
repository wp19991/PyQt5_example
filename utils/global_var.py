# 全局变量管理模块
def __init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, default_value=None):
    return _global_dict.get(name, default_value)
