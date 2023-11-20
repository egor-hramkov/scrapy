def str_to_int(x):
    try:
        return int(float(x))
    except:
        return x


def list_to_str(lst: list) -> str:
    return ' '.join(lst)


class StripText:
    def __init__(self, chars=' rtn'):

        self.chars = chars

    def __call__(self, value):
        try:
            return value.strip(self.chars)
        except:
            return value

def parse_time(elapsed_time: int) -> str:
    """Преобразует время в секундах в другой формат"""
    return str(datetime.timedelta(seconds=elapsed_time))