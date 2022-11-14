import re


def verify_email(str):
    pass


def verify_passwd(str):
    pass


def verify_str_type(str):
    pass


def verify_dict_type(str):
    pass


def verify_int_type(param):
    if param:
        if not isinstance(param, int):
            try:
                param = int(param)
            except Exception as e:
                raise ValueError('{} must be int type'.format(param))
        else:
            return param
    else:
        return param


def verify_fload_type(str):
    pass


def verify_list_type(str):
    pass
