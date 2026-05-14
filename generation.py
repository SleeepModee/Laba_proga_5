import csv
import random
import string
import os

# Настройки генерации
FILENAME = "mmo_stats.csv"
TARGET_SIZE_GB = 1.0
TARGET_SIZE_BYTES = TARGET_SIZE_GB * 1024 * 1024 * 1024
CHUNK_SIZE = 50000  # Размер пачки строк в памяти

def generate_random_name():
    """Генерирует случайное имя игрока от 5 до 12 символов."""
    length = random.randint(5, 12)
    # Используем буквы ASCII для генерации
    return ''.join(random.choices(string.ascii_letters, k=length)).capitalize()

def generate_chunk(num_rows):
    """Генерирует пачку данных, чтобы не хранить всё в ОЗУ."""
    chunk = []
    for _ in range(num_rows):
        name = generate_random_name()
        level = random.randint(1, 100)
        win_rate = round(random.uniform(10.0, 90.0), 2)  # Дробное число с 2 знаками
        is_banned = random.choice([True, False])
        
        # Генерируем случайную дату в формате YYYY-MM-DD
        year = random.randint(2020, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        last_login = f"{year}-{month:02d}-{day:02d}"

        chunk.append([name, level, win_rate, is_banned, last_login])
    return chunk

def main():
    print(f"Начинаем генерацию файла {FILENAME} (Цель: {TARGET_SIZE_GB} ГБ)...")
    
    # Открываем файл на запись ('w'). newline='' нужен для правильной работы модуля csv
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Записываем заголовки колонок
        writer.writerow(["Character_Name", "Level", "Win_Rate", "Is_Banned", "Last_Login"])

        current_size = 0
        while current_size < TARGET_SIZE_BYTES:
            # Генерируем и записываем чанк
            chunk = generate_chunk(CHUNK_SIZE)
            writer.writerows(chunk)
            
            # Принудительно сбрасываем данные из буфера ОС на жесткий диск
            f.flush() 
            
            # Обновляем текущий размер файла
            current_size = os.path.getsize(FILENAME)
            
            # Выводим прогресс в консоль (возврат каретки \r перезаписывает строку)
            print(f"Сгенерировано: {current_size / (1024*1024):.2f} МБ", end='\r')
            
    print(f"\nГотово! Итоговый размер файла: {os.path.getsize(FILENAME) / (1024*1024*1024):.2f} ГБ")

if __name__ == '__main__':
    main()