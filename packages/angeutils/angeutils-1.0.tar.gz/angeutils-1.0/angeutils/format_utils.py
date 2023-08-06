import json


def dict2json(dict_data):
    return json.dumps(dict_data)


def json2dict(json_data):
    return json.loads(json_data)


#### 带颜色的控制台输出 ####
class _DisplayMethod:
    DEFAULT = 0
    HIGHLIGHT = 1
    UNDERLINE = 4
    BLINK = 5


class _TextColor:
    RED = 31
    GREEN = 32
    YELLOW = 33


# BG_COLOR_BLACK = 40
# BG_COLOR_RED = 41
DISPLAY_METHOD = _DisplayMethod()
TEXT_COLOR = _TextColor()


def colored_string(raw_str, display_method=DISPLAY_METHOD.DEFAULT, text_color=TEXT_COLOR.RED):
    colored_str = f"\033[{display_method};{text_color}m {raw_str}\033[0m"
    return colored_str

#### 带颜色的控制台输出 ####