from datetime import datetime
from functools import wraps


def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        log_res = (f'Дата и время вызова функции: {datetime.now()}, '
                   f'имя функции: {old_function.__name__}, '
                   f'аргументы функции: {args}, {kwargs} '
                   f'возвращаемое значение функции: '
                   f'{old_function(*args, **kwargs)}\n')
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(log_res)
        return old_function(*args, **kwargs)
    return new_function
