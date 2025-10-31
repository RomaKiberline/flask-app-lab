#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки функціоналу Lab 4
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:5000"

def test_login_page():
    """Тест 1: Перевірка доступності сторінки входу"""
    print("🔍 Тест 1: Перевірка сторінки входу...")
    response = requests.get(f"{BASE_URL}/users/login")
    assert response.status_code == 200
    assert "Вхід в систему" in response.text
    print("✅ Сторінка входу доступна")

def test_login_invalid():
    """Тест 2: Перевірка невірних даних входу"""
    print("\n🔍 Тест 2: Перевірка невірних даних входу...")
    session = requests.Session()
    response = session.post(f"{BASE_URL}/users/login", data={
        'username': 'invalid',
        'password': 'wrong'
    }, allow_redirects=True)
    assert ("Невірне ім'я користувача або пароль" in response.text or 
            "Невірне ім&#39;я користувача або пароль" in response.text)
    print("✅ Flash повідомлення про помилку відображається")

def test_login_valid():
    """Тест 3: Перевірка правильних даних входу"""
    print("\n🔍 Тест 3: Перевірка правильних даних входу...")
    session = requests.Session()
    response = session.post(f"{BASE_URL}/users/login", data={
        'username': 'admin',
        'password': 'admin123'
    }, allow_redirects=True)
    assert "Ласкаво просимо" in response.text
    assert "Вітаємо, admin!" in response.text
    print("✅ Успішний вхід і перенаправлення на профіль")
    return session

def test_profile_access_without_login():
    """Тест 4: Перевірка доступу до профілю без входу"""
    print("\n🔍 Тест 4: Перевірка доступу до профілю без входу...")
    response = requests.get(f"{BASE_URL}/users/profile", allow_redirects=True)
    assert "Будь ласка, увійдіть в систему" in response.text
    print("✅ Перенаправлення на сторінку входу з повідомленням")

def test_cookie_management(session):
    """Тест 5: Перевірка управління cookies"""
    print("\n🔍 Тест 5: Перевірка управління cookies...")
    
    # Додавання cookie
    response = session.post(f"{BASE_URL}/users/add-cookie", data={
        'key': 'test_key',
        'value': 'test_value',
        'max_age': '3600'
    }, allow_redirects=True)
    assert ('Cookie "test_key" додано' in response.text or 
            'Cookie &#34;test_key&#34; додано' in response.text)
    print("✅ Cookie успішно додано")
    
    # Перевірка відображення cookie
    response = session.get(f"{BASE_URL}/users/profile")
    assert 'test_key' in response.text
    assert 'test_value' in response.text
    print("✅ Cookie відображається в таблиці")
    
    # Видалення cookie
    response = session.get(f"{BASE_URL}/users/delete-cookie/test_key", allow_redirects=True)
    assert ('Cookie "test_key" видалено' in response.text or 
            'Cookie &#34;test_key&#34; видалено' in response.text)
    print("✅ Cookie успішно видалено")

def test_color_scheme(session):
    """Тест 6: Перевірка зміни кольорової схеми"""
    print("\n🔍 Тест 6: Перевірка зміни кольорової схеми...")
    
    # Встановлення темної теми
    response = session.get(f"{BASE_URL}/users/set-color-scheme/dark", allow_redirects=True)
    assert ('Кольорову схему змінено на "dark"' in response.text or 
            'Кольорову схему змінено на &#34;dark&#34;' in response.text)
    assert 'dark-theme' in response.text
    print("✅ Темна тема встановлена")
    
    # Встановлення світлої теми
    response = session.get(f"{BASE_URL}/users/set-color-scheme/light", allow_redirects=True)
    assert ('Кольорову схему змінено на "light"' in response.text or 
            'Кольорову схему змінено на &#34;light&#34;' in response.text)
    assert 'light-theme' in response.text
    print("✅ Світла тема встановлена")

def test_logout(session):
    """Тест 7: Перевірка виходу з системи"""
    print("\n🔍 Тест 7: Перевірка виходу з системи...")
    response = session.get(f"{BASE_URL}/users/logout", allow_redirects=True)
    assert "До побачення" in response.text
    print("✅ Вихід з системи успішний")

def test_flash_messages():
    """Тест 8: Перевірка flash повідомлень"""
    print("\n🔍 Тест 8: Перевірка flash повідомлень...")
    session = requests.Session()
    
    # Помилка входу
    response = session.post(f"{BASE_URL}/users/login", data={
        'username': 'wrong',
        'password': 'wrong'
    }, allow_redirects=True)
    assert 'flash-error' in response.text
    print("✅ Flash повідомлення з категорією 'error' працює")
    
    # Успішний вхід
    response = session.post(f"{BASE_URL}/users/login", data={
        'username': 'admin',
        'password': 'admin123'
    }, allow_redirects=True)
    assert 'flash-success' in response.text
    print("✅ Flash повідомлення з категорією 'success' працює")

def main():
    print("=" * 60)
    print("🧪 ТЕСТУВАННЯ ЛАБОРАТОРНОЇ РОБОТИ №4")
    print("=" * 60)
    
    try:
        test_login_page()
        test_login_invalid()
        session = test_login_valid()
        test_profile_access_without_login()
        test_cookie_management(session)
        test_color_scheme(session)
        test_logout(session)
        test_flash_messages()
        
        print("\n" + "=" * 60)
        print("✅ ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ ТЕСТ ПРОВАЛЕНО: {e}")
    except Exception as e:
        print(f"\n❌ ПОМИЛКА: {e}")

if __name__ == "__main__":
    main()
