from utils import _thread_local


class GlobalsContext:

    __storage__ = _thread_local()

    def push(self):
        self.__storage__ = {}

    def pop(self):
        self.__storage__.clear()

    def __setattr__(self, attr, value):
        if attr == '__storage__':
            super().__setattr__(attr, value)
        self.__storage__[attr] = value

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, *args):
        self.pop

    def __getattr__(self, attr):
        if attr in self.__storage__:
            return self.__storage__.get(attr)
        return super().__getattr__(attr)
