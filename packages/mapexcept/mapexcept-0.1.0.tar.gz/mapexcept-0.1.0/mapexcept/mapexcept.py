import typing
import onetrick

@onetrick
class MapExcept:
    def __init__(self, __func:typing.Callable, *__iterables:typing.Iterable):
        self.exceptions = list()

        self.func = __func
        self.iterables = __iterables

    def __getitem__(self, exception_type:typing.Type[Exception]):
        self.exceptions.append(exception_type)
        return self
    
    def __iter__(self):
        exceptions = tuple(self.exceptions)

        for args in zip(*self.iterables):
            value:object

            try:
                value = self.func(*args)
            except exceptions:
                continue
        
            yield value
    