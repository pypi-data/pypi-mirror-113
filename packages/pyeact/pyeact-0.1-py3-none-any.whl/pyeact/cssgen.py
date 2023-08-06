class CSSObject(object):
    def __init__(self, key="", value=""):
        self.key = key
        self.value = value

    def __str__(self):
        if type(self.value) != list and type(self.value) != tuple:
            return f"{self.key}: {self.value};"
        else:
            values = ""
            for i in list(self.value):
                values += f" {i}"
            return f"{self.key}:{values};"


class CSSGen(object):
    def __getattr__(self, item):
        return lambda value: CSSObject(item, value)
