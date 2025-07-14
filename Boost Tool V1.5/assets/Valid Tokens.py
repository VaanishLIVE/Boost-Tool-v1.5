import requests

def check_token(token):
    # URL для получения информации о текущем пользователе
    url = "https://discord.com/api/v9/users/@me"
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

    # Статус 200 означает, что токен валидный
    if response.status_code == 200:
        return True
    # Статус 401 (Unauthorized) означает, что токен невалидный
    elif response.status_code == 401:
        return False
    else:
        print(f"Неожиданный ответ сервера: {response.status_code}")
        return None

def main():
    token = input("Введите Discord токен для проверки: ").strip()

    valid = check_token(token)
    
    if valid is True:
        print("Токен валидный!")
    elif valid is False:
        print("Токен невалидный!")
    else:
        print("Не удалось проверить токен.")

if __name__ == '__main__':
    main()