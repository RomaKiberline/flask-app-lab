# Flask App - Лабораторна робота №3

Flask додаток зі структурою на основі Blueprints.

## Структура проекту

```
flask_app_chupyrchuk/
├── app/
│   ├── __init__.py          # Ініціалізація додатку та реєстрація blueprints
│   ├── users/               # Blueprint для користувачів
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── templates/
│   │       └── users/
│   │           └── hi.html
│   ├── products/            # Blueprint для продуктів
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── templates/
│   │       └── products/
│   │           └── product.html
│   ├── templates/           # Базові шаблони
│   │   └── base.html
│   └── static/              # Статичні файли (CSS, JS)
├── tests/                   # Модульні тести
│   ├── test_user_bp.py
│   └── test_product_bp.py
├── config.py                # Конфігурація додатку
├── run.py                   # Точка входу
└── requirements.txt
```

## Встановлення

1. Активуйте віртуальне середовище:
```bash
source venv/bin/activate
```

2. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Конфігурація

Додаток підтримує різні режими роботи через `config.py`:

- **Development** (за замовчуванням) - режим розробки з DEBUG=True
- **Testing** - режим для тестування
- **Production** - режим для продакшену

Змінити режим можна через змінну середовища:
```bash
export FLASK_ENV=production
```

## Запуск додатку

```bash
python run.py
# або
./venv/bin/python run.py
```

Додаток буде доступний за адресою: http://localhost:5000

## Доступні маршрути

- `/` - Головна сторінка з посиланнями на всі розділи
- `/users/hi/<name>?age=<age>` - Привітання користувача
- `/users/admin` - Перенаправлення на адміністратора
- `/products/` - Список продуктів

## Запуск тестів

```bash
python -m unittest discover tests -v
# або
./venv/bin/python -m unittest discover tests -v
```
