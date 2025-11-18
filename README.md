# Banking operations widget

Программа для фильтрации и сортировки банковских операций по дате и статусу оплаты.  
Также есть функции маскировки номеров карт и счетов.

## Зависимости
- Python 3.12
- flake8 = "7.1.0"
- black = "24.4.2"
- isort = "5.13.2"
- mypy = "1.10.0"
- pytest

## Что умеет программа
- маскировать номера карт и счетов;
- сортировать операции по дате (по возрастанию/убыванию);
- фильтровать операции по статусу.

## Новый модуль: `generators`

Добавлен модуль `generators`, который помогает работать с большим количеством транзакций с помощью генераторов.

Функции модуля:

- `filter_by_currency(transactions, currency_code="USD")`  
  Возвращает только те транзакции, где валюта совпадает с указанной.

- `transaction_descriptions(transactions)`  
  Генератор, который по очереди возвращает описание каждой операции.  
  Пропускает пустые описания и записи без данных об операции.

- `card_number_generator(start, end)`  
  Генерирует номера банковских карт в формате `XXXX XXXX XXXX XXXX`  
  в заданном диапазоне (включительно).  
  Например: `"0000 0000 0000 0001"`.

## Новый модуль: `decorators`

Декоратор `log` логирует вызовы функций:
- если передан `filename`, пишет логи в файл;
- если `filename` не указан — выводит в консоль.

Пример:
```python
from chunaev_aa_homework import log

@log()  # лог в консоль
def add(a, b):
    return a + b

@log(filename="app.log")  # лог в файл
def mul(a, b):
    return a * b

### Пример использования:

```python
from chunaev_aa_homework import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

transactions = [
    {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}, "description": "Перевод"},
    {"operationAmount": {"amount": "250.00", "currency": {"code": "RUB"}}, "description": "Оплата"},
]

print(list(filter_by_currency(transactions, "USD")))
print(list(transaction_descriptions(transactions)))
print(list(card_number_generator(1, 3)))

## Работа с CSV и Excel

Проект умеет считывать финансовые операции из файлов форматов
CSV и Excel.

Новые функции находятся в модуле `utils_io`:

- `read_csv_operations(path)` — читает CSV-файл и возвращает список
  словарей с транзакциями.
- `read_xlsx_operations(path)` — читает Excel-файл и возвращает список
  словарей с транзакциями.

## Установка
Склонировать репозиторий:


```git clone https://github.com/Artemhio/chunaev_aa_homework.git```

Установить зависимости:

```pip install -r requirements.txt```

Тестирование

Для тестов используется pytest.
Запуск:

```pytest -v```

Подождите, пока наборы данных загрузятся, это может занять некоторое время. 

В тестах используются фикстуры для генерации данных и параметризация для проверки разных кейсов.

Проверка качества кода

Запустить линтеры и форматеры:

```flake8 src tests
mypy src
isort .
black .
```
Все тесты должны проходить ✅
Покрытие тестами > 80%.

Можно получить html-отчёт:

```pytest --cov=src --cov-report=html```

После этого в папке htmlcov/ появится файл index.html, который можно открыть в браузере.

В тестах используются фикстуры для генерации данных и параметризация для проверки разных кейсов.

## Команда проекта:

`Чунаев Артем - student ` 

## Контакт для связи с командой разработки:

`artemiy9999@gmail.com` 

`Discord - artemhio`

## Источники

Материалы для изучения SKYPRO [skypro@skyeng.ru](https://sky.pro/#giftpopup)