import datetime
import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования вызовов функции (в консоль или в файл)."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = ""
            try:
                result = func(*args, **kwargs)
                message = (
                    f"[{timestamp}] Function '{func.__name__}' executed "
                    f"successfully. Result: {result}\n"
                )
                return result
            except Exception as e:
                message = (
                    f"[{timestamp}] Function '{func.__name__}' raised "
                    f"{type(e).__name__} with args={args}, kwargs={kwargs}\n"
                )
                # печатаем/пишем лог и снова пробрасываем ошибку
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message)
                else:
                    print(message.strip())
                raise
            finally:
                # общая точка записи лога при успехе
                if message and not filename:
                    print(message.strip())
                elif message and filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message)

        return wrapper

    return decorator
