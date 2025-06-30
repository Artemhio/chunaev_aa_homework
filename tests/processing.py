# Пример операции
from src.widget import mask_account_card, get_data

operation = {
    "date": "2023-10-05T16:20:00.000000Z",
    "description": "Перевод с карты на карту",
    "from": "Visa Platinum 1234567890123456",
    "to": "Счет 12345678901234567890",
    "amount": "1000.00",
    "currency": "RUB"
}

# Обработка
formatted_operation = {
    "date": get_data(operation["date"]),
    "description": operation["description"],
    "from": mask_account_card(operation["from"]),
    "to": mask_account_card(operation["to"]),
    "amount": f"{operation['amount']} {operation['currency']}"
}

print(formatted_operation)
"""
{
    'date': '05.10.2023',
    'description': 'Перевод с карты на карту',
    'from': 'Visa Platinum 1234 56** **** 3456',
    'to': 'Счет **7890',
    'amount': '1000.00 RUB'
}
"""