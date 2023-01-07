import datetime
import os

def logger(func):
    def new_function(*args, **kwargs):
        old_function = func(*args, **kwargs)
        log_line = f'{datetime.datetime.now()} функция: {func.__name__}; аргументы: {str(args)}, {str(kwargs)}; вернула результат:{str(old_function)}.\n'
        with open(f'log_{datetime.datetime.today().strftime("%d_%m_%Y")}.txt', 'a') as log_file:
            log_file.write(log_line)
        return old_function
    return new_function

def parametr_logger(path, echo=False, mode='a'):
    def decorator(func):
        def new_function(*args, **kwargs):
            old_function = func(*args, **kwargs)
            log_line = f'{datetime.datetime.now()} функция: {func.__name__}; аргументы: {str(args)}, {str(kwargs)}; вернула результат:{str(old_function)}.\n'
            with open(path,  mode) as log_file:
                log_file.write(log_line)
            if echo:
                print(log_line)
            return old_function
        return new_function
    return decorator


def test_1():
    path = f'log_{datetime.datetime.today().strftime("%d_%m_%Y")}.txt'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @parametr_logger(path)
        def hello_world():
            return 'Hello World'

        @parametr_logger(path)
        def summator(a, b=0):
            return a + b

        @parametr_logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    test_2()