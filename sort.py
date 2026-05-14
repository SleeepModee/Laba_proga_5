import csv
import os
import time
import heapq
import sys

# Считываем режим сортировки от GUI (по умолчанию level)
sort_mode = sys.argv[1] if len(sys.argv) > 1 else "level"

# Единая функция для получения ключа сортировки
def get_sort_key(row):
    if sort_mode == "name":
        return row[0] # Индекс 0 - Имя (строка)
    elif sort_mode == "winrate":
        return float(row[2]) # Индекс 2 - Винрейт (дробное число)
    else:
        return int(row[1]) # Индекс 1 - Уровень (целое число)

# Нужно ли переворачивать сортировку? (Имена сортируем А-Я, а числа по убыванию)
is_reverse = False if sort_mode == "name" else True

def external_sort_python():
    input_file = "mmo_stats.csv"
    output_file = "sorted_python.csv"
    chunk_folder = "chunk_py" 

    print(f"=== СТАРТ PYTHON СОРТИРОВКИ (Поле: {sort_mode}) ===")
    start_time = time.time()

    # Просим Питон сам создать папку для чанков, если её нет
    if not os.path.exists(chunk_folder):
        os.makedirs(chunk_folder)

    chunk_filenames = []

    # ==========================================
    # ЭТАП 1: РАЗБИЕНИЕ НА ЧАНКИ
    # ==========================================
    print("Этап 1: Читаем файл и нарезаем на чанки...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader) 

        chunk = []
        chunk_index = 0

        for row in reader:
            chunk.append(row)
            
            if len(chunk) == 100000:
                # Сортируем с учетом выбранного ключа
                chunk.sort(key=get_sort_key, reverse=is_reverse)
                
                chunk_name = f"{chunk_folder}/chunk_{chunk_index}.csv"
                with open(chunk_name, 'w', encoding='utf-8', newline='') as chunk_file:
                    writer = csv.writer(chunk_file)
                    writer.writerows(chunk)
                
                chunk_filenames.append(chunk_name) 
                chunk.clear() 
                chunk_index += 1

        if chunk:
            chunk.sort(key=get_sort_key, reverse=is_reverse)
            chunk_name = f"{chunk_folder}/chunk_{chunk_index}.csv"
            with open(chunk_name, 'w', encoding='utf-8', newline='') as chunk_file:
                writer = csv.writer(chunk_file)
                writer.writerows(chunk)
            chunk_filenames.append(chunk_name)

    split_time = time.time()
    print(f"Разбиение завершено! Создано файлов: {len(chunk_filenames)}")


    # ==========================================
    # ЭТАП 2: МНОГОПУТЕВОЕ СЛИЯНИЕ
    # ==========================================
    print("Этап 2: Сливаем чанки в итоговый файл...")
    
    file_objects = [open(name, 'r', encoding='utf-8') for name in chunk_filenames]
    readers = [csv.reader(f) for f in file_objects]

    with open(output_file, 'w', encoding='utf-8', newline='') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)

        # Сливаем с учетом выбранного ключа
        merged_data = heapq.merge(*readers, key=get_sort_key, reverse=is_reverse)
        writer.writerows(merged_data)

    # ==========================================
    # ЭТАП 3: УБОРКА
    # ==========================================
    for f, name in zip(file_objects, chunk_filenames):
        f.close()      
        os.remove(name) 
        
    os.rmdir(chunk_folder) 

    end_time = time.time()
    print("ГОТОВО! Файл sorted_python.csv успешно создан.")
    print(f"Общее время работы: {round(end_time - start_time, 2)} секунд.")

if __name__ == "__main__":
    external_sort_python()