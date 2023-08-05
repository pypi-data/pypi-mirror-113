def strict(func):
    def wrapper(*args, **kwargs):
        del_array = []

        for (name, type_), j in zip(func.__annotations__.items(), args):
            if type_ != type(j):
                raise TypeError()
            else:
                del_array.append(name)
        for name in del_array:
            func.__annotations__.pop(name)

        for (name, type_), (key, value) in zip(func.__annotations__.items(), kwargs.items()):
            if type_ != type(value):
                raise TypeError()

        res = func(*args, **kwargs)

        if 'return' in func.__annotations__.keys() and type(res) != func.__annotations__['return']:
            raise TypeError()

        return res

    return wrapper


@strict
def test(a: int, b: int) -> int:
    return a + b


print('Res:', test(2.5, b=2))
