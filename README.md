# parse-medrocket

Парсер вакансий с сайта MedRocket с автоматическим мониторингом и логированием.

## Что делает

Периодически проверяет страницу вакансий, ищет позиции по ключевым словам
(`Backend`, `Django`, `Python`). При нахождении — записывает результат
в файл для последующей отправки через Telegram-бота.

## Стек

- Python 3.11+
- requests
- BeautifulSoup4
- logging

## Быстрый старт
```bash
git clone https://github.com/KuPriv/parse-medrocket.git
cd parse-medrocket
pip install -r requirements.txt
cp .env.example .env
# заполнить .env своими значениями
python try_to_parse.py
```

## Пример работы
```
2025-03-05 10:06:00 INFO set_logging_settings   Были добавлены настройки конфигурации logging.
2025-03-05 10:06:00 INFO get_headers_for_request Создана хэш-таблица с заголовками для парсинга.
2025-03-05 10:06:00 INFO retrieve_response_from_site Получен ответ с сайта. 200
2025-03-05 10:06:00 INFO check_vacancies  Была найдена вакансия: Вакансия Junior Python разработчик
2025-03-05 10:06:00 INFO write_status_indicator  Записали вакансию в file в dir: tg_bot
```

## Структура
```
parse-medrocket/
├── tg_bot/
│   ├── main.py               # Telegram-бот с планировщиком
│   └── status_indicator.txt  # Результат для передачи боту
├── logs_here/
│   └── logs.log              # История запросов
├── try_to_parse.py           # Основной модуль парсера
├── .env.example              # Шаблон переменных окружения
└── requirements.txt
```