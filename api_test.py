import requests

# Адрес вашего локального сервера
BASE_URL = "http://127.0.0.1:8000/api/v1/"

# Логин и пароль администратора, созданного через createsuperuser
# Измените их на свои реальные данные перед запуском
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_password"

def run_tests():
    print("=== НАЧАЛО ТЕСТИРОВАНИЯ API ===\n")

    # 1. Тестирование поиска (GET с параметром ?search)
    search_term = "Книги"
    print(f"1. Тестирование поиска категорий по слову: '{search_term}'...")
    try:
        response = requests.get(f"{BASE_URL}categories/?search={search_term}")
        if response.status_code == 200:
            data = response.json()
            print(f"Успешно. Найдено записей: {data.get('count', 0)}")
            for item in data.get('results', []):
                print(f" - ID: {item['id']} | Название: {item['name']}")
        else:
            print(f"Ошибка выполнения запроса: {response.status_code}")
    except Exception as e:
        print(f"Не удалось подключиться к серверу: {e}")
        return

    print("\n--------------------------------------------------\n")

    # 2. Тестирование динамической пагинации (?page_size=X)
    page_size = 2
    print(f"2. Запрос списка снаряжения с лимитом {page_size} элементов на страницу...")
    response = requests.get(f"{BASE_URL}equipment/?page_size={page_size}")
    if response.status_code == 200:
        data = response.json()
        print(f"Успешно. Всего элементов в базе: {data.get('count', 0)}")
        print(f"Выведено на этой странице: {len(data.get('results', []))}")
        for item in data.get('results', []):
            print(f" - Снаряжение: {item['name']} | Цена: {item['price']} Ankh")
    else:
        print(f"Ошибка пагинации: {response.status_code}")

    print("\n--------------------------------------------------\n")

    # 3. Проверка прав доступа (Попытка анонимного создания записи)
    print("3. Попытка анонимного добавления новой категории (ожидается отказ)...")
    payload = {
        "name": "Запретное снаряжение",
        "description": "Попытка несанкционированной записи данных"
    }
    response = requests.post(f"{BASE_URL}categories/", json=payload)
    print(f"Статус ответа сервера: {response.status_code}")
    if response.status_code == 403:
        print("Успешно: Сервер отклонил анонимный POST-запрос (403 Forbidden).")
    else:
        print("Внимание: Настройки прав доступа не сработали.")

    print("\n--------------------------------------------------\n")

    # 4. Авторизованное добавление записи (POST с базовой авторизацией)
    print("4. Авторизованное добавление категории под учетной записью администратора...")
    auth_credentials = (ADMIN_USERNAME, ADMIN_PASSWORD)
    payload_auth = {
        "name": "Новое Оружие",
        "description": "Категория добавлена программно через API-тест"
    }
    response = requests.post(f"{BASE_URL}categories/", json=payload_auth, auth=auth_credentials)
    print(f"Статус ответа сервера: {response.status_code}")
    if response.status_code == 201:
        created_data = response.json()
        print("Успешно: Новая категория создана!")
        print(f"Созданный объект: ID {created_data['id']} | Название: {created_data['name']}")
    elif response.status_code == 401:
        print("Ошибка: Неверные учетные данные администратора. Измените логин/пароль в скрипте.")
    else:
        print(f"Не удалось создать категорию: {response.text}")

    print("\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")

if __name__ == "__main__":
    run_tests()