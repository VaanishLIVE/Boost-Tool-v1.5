import os
import sys
import time
import random
import ctypes
import logging
from typing import List, Optional

# Цвета ANSI (оптимизированы для скорости)
COLORS = {
    'red': "\033[31m",
    'white': "\033[37m",
    'cyan': "\033[36m",
    'purple': "\033[35m",
    'green': "\033[32m",
    'reset': "\033[0m"
}

# Обновленный предварительно скомпилированный баннер (шрифт 'speed')
PRECOMPILED_BANNER = r"""
          ____                  _     _____           _ 
         | __ )  ___   ___  ___| |_  |_   _|__   ___ | |
         |  _ \ / _ \ / _ \/ __| __|   | |/ _ \ / _ \| |
         | |_) | (_) | (_) \__ \ |_    | | (_) | (_) | |
         |____/ \___/ \___/|___/\__|   |_|\___/ \___/|_|
""".strip()

# Настройки консоли
CONSOLE_WIDTH = 80
SIMULATION_MODE = True
BANNER_CACHE = {} # В данном случае не используется, так как баннер предкомпилирован

def set_console_title(title: str):
    """Установка заголовка консоли (только Windows)"""
    try:
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(title)
    except Exception as e:
        logging.error(f"Ошибка установки заголовка: {e}")

def clear_console():
    """Оптимизированная очистка консоли"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        logging.error(f"Ошибка очистки консоли: {e}")

def fast_print(text: str = "", end: str = "\n"):
    """Мгновенный вывод с обработкой ошибок"""
    try:
        sys.stdout.write(text + end)
        sys.stdout.flush()
    except Exception as e:
        logging.error(f"Ошибка вывода: {e}")

def generate_banner(font: str = 'slant') -> str:
    """Генерация баннера с обработкой ошибок (оригинальная функция, не используется для PRECOMPILED_BANNER)"""
    if font in BANNER_CACHE:
        return BANNER_CACHE[font]
    
    try:
        from pyfiglet import Figlet
        f = Figlet(font=font)
        banner = f.renderText("Boost Tool")
    except ImportError:
        banner = "Boost Tool"
    except Exception as e:
        banner = "Boost Tool"
        logging.error(f"Ошибка генерации баннера: {e}")
    
    BANNER_CACHE[font] = banner
    return banner

def print_title():
    """Максимально быстрый вывод баннера"""
    clear_console()
    
    try:
        # Упрощено: используем фиксированную ширину, чтобы избежать ошибок с os.get_terminal_size()
        console_width = CONSOLE_WIDTH

        banner = PRECOMPILED_BANNER
        lines = banner.split('\n')
        half = len(lines) // 2
        
        for i, line in enumerate(lines):
            # Изменено на красно-белый цвет
            color = COLORS['red'] if i < half else COLORS['white']
            fast_print(color + line.center(console_width) + COLORS['reset'])
        
        # Обновлена версия
        fast_print(COLORS['white'] + "Version: 1.5".center(console_width) + COLORS['reset'])
        fast_print(COLORS['white'] + "".rjust(console_width) + COLORS['reset'])
        fast_print()
    except Exception as e:
        fast_print(COLORS['red'] + f"Ошибка вывода заголовка: {e}" + COLORS['reset'])
        logging.error(f"Ошибка вывода заголовка: {e}")

def validate_url(url: str) -> bool:
    """Проверка URL формата"""
    return url.startswith("https://discord.gg/")

def get_tokens() -> List[str]:
    """Ввод и валидация токенов"""
    try:
        input_str = input(COLORS['white'] + "Введите токены (через пробел): " + COLORS['reset']).strip()
        return input_str.split() if input_str else ["fake_token"]
    except Exception as e:
        logging.error(f"Ошибка ввода токенов: {e}")
        return []

def check_token(token: str) -> str:
    """Оптимизированная проверка токена"""
    if SIMULATION_MODE or "fake" in token:
        return "valid_nitro"
    
    try:
        import requests
        response = requests.get(
            "https://discord.com/api/v9/users/@me",
            headers={"Authorization": token},
            timeout=5
        )
        return "valid_nitro" if response.status_code == 200 else "invalid"
    except Exception as e:
        logging.error(f"Ошибка проверки токена: {e}")
        return "error"

def process_boosts(tokens: List[str], count: int, action: str):
    """Универсальная функция для буста/анбуста"""
    valid_tokens = [t for t in tokens if check_token(t) == "valid_nitro"]
    
    if not valid_tokens:
        fast_print(COLORS['red'] + " Нет валидных токенов с Nitro!" + COLORS['reset'])
        return
    
    action_text = "Буст" if action == "boost" else "Снятие буста"
    fast_print(COLORS['white'] + f" Найдено {len(valid_tokens)} валидных токенов." + COLORS['reset'])
    fast_print(COLORS['white'] + f" Начинаем {action_text}..." + COLORS['reset'])
    
    for token in valid_tokens:
        for _ in range(count):
            # Имитация успеха/ошибки
            if random.random() < 0.1:
                fast_print(COLORS['red'] + f" Ошибка при {action_text} токеном {token[:6]}..." + COLORS['reset'])
            else:
                fast_print(COLORS['green'] + f" Успешно {action_text} токеном {token[:6]}..." + COLORS['reset'])
            time.sleep(0.1) # Небольшая задержка для имитации работы

def main_menu():
    """Меню с анимированным заголовком"""
    print_title()
    
    menu_items = [
        (f"{COLORS['red']}[{COLORS['white']}1{COLORS['red']}]{COLORS['reset']} {COLORS['white']}Boost Tool{COLORS['reset']}", ""),
        (f"{COLORS['red']}[{COLORS['white']}2{COLORS['red']}]{COLORS['reset']} {COLORS['white']}Unboost{COLORS['reset']}", ""),
        (f"{COLORS['red']}[{COLORS['white']}0{COLORS['red']}]{COLORS['reset']} {COLORS['white']}Выход{COLORS['reset']}", "")
    ]
    
    for item, emoji in menu_items:
        fast_print(f"{emoji} {item}")
    fast_print()

def main():
    """Основной цикл программы"""
    # Обновлен заголовок консоли
    set_console_title("Boost Tool I Version: 1.5") 
    
    while True:
        try:
            main_menu()
            choice = input(COLORS['white'] + "🔘 Выберите действие: " + COLORS['reset']).strip()
            
            if choice == "1":
                fast_print(COLORS['white'] + " Введите URL сервера: " + COLORS['reset'])
                url = input().strip()
                if not validate_url(url):
                    fast_print(COLORS['red'] + " Неверный формат URL!" + COLORS['reset'])
                    continue
                
                fast_print(COLORS['white'] + " Введите количество бустов: " + COLORS['reset'])
                try:
                    count = int(input())
                    process_boosts(get_tokens(), count, "boost")
                except ValueError:
                    fast_print(COLORS['red'] + " Введите число!" + COLORS['reset'])
            
            elif choice == "2":
                fast_print(COLORS['white'] + " Введите количество снятий: " + COLORS['reset'])
                try:
                    count = int(input())
                    process_boosts(get_tokens(), count, "unboost")
                except ValueError:
                    fast_print(COLORS['red'] + " Введите число!" + COLORS['reset'])
            
            elif choice == "0":
                fast_print(COLORS['white'] + " Выход из программы..." + COLORS['reset'])
                break
            
            else:
                fast_print(COLORS['red'] + " Неверный выбор!" + COLORS['reset'])
            
            time.sleep(1)
        
        except KeyboardInterrupt:
            fast_print("\n Выход из программы...")
            break
        except Exception as e:
            fast_print(COLORS['red'] + f" Критическая ошибка: {e}" + COLORS['reset'])
            logging.error(f"Критическая ошибка: {e}")
            input(COLORS['white'] + "\nНажмите Enter для продолжения..." + COLORS['reset'])  # Заменил sleep на input для удержания окна

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        fast_print(COLORS['red'] + f" Фатальная ошибка: {e}" + COLORS['reset'])
        logging.error(f"Фатальная ошибка: {e}")
    finally:
        input(COLORS['white'] + "\nНажмите Enter для выхода..." + COLORS['reset'])
