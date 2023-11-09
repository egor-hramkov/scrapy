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
