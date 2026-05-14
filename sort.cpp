#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <windows.h>
#include <queue>   
#include <ctime>   
#include <cstdio>  

using namespace std;

// Глобальная переменная для режима сортировки
// 1 = Уровень (по убыванию), 2 = Имя (А-Я), 3 = Винрейт (по убыванию)
int current_sort_mode = 1; 

// === СТРУКТУРЫ ===
struct Stats {
    string name;
    int level;
    double winrate;
    bool ban;
    string lastlogin;
};

struct QueueNode {
    Stats player;
    int file_index; 
};

// --- ПРАВИЛА СОРТИРОВКИ ---

// Правило для первичной сортировки кусочков (чанков)
bool CustomSort(const Stats& a, const Stats& b) {
    if (current_sort_mode == 2) return a.name < b.name;       // Имя: от А до Я
    if (current_sort_mode == 3) return a.winrate > b.winrate; // Винрейт: от большего к меньшему
    return a.level > b.level;                                 // Уровень: от большего к меньшему (по умолчанию)
}

// Правило для Очереди (в priority_queue знаки ставятся НАОБОРОТ)
struct CompareNode {
    bool operator()(const QueueNode& a, const QueueNode& b) {
        if (current_sort_mode == 2) return a.player.name > b.player.name;       
        if (current_sort_mode == 3) return a.player.winrate < b.player.winrate; 
        return a.player.level < b.player.level;                                 
    }
};

// === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
Stats parseCSV(const string& line) {
    Stats player;
    stringstream ss(line);
    string token;
    getline(ss, player.name, ',');
    
    getline(ss, token, ','); player.level = stoi(token);
    getline(ss, token, ','); player.winrate = stod(token);
    getline(ss, token, ','); player.ban = (token == "True");
    
    getline(ss, player.lastlogin, ',');
    return player;
}

void saveChunk(const vector<Stats>& chunk, const string& filename) {
    ofstream outFile(filename);
    outFile << "Character_Name,Level,Win_Rate,Is_Banned,Last_Login\n";
    for (const auto& player : chunk) {
        outFile << player.name << "," << player.level << ","
                << player.winrate << "," << (player.ban ? "True" : "False") << ","
                << player.lastlogin << "\n";
    }
    outFile.close();
}

// === ФУНКЦИЯ СЛИЯНИЯ ===
void mergeChunks(int total_chunks, const string& output_filename) {
    vector<ifstream> files(total_chunks);
    priority_queue<QueueNode, vector<QueueNode>, CompareNode> pq;

    // 1. Открываем чанки и берем по одной строке
    for (int i = 0; i < total_chunks; ++i) {
        string filename = "chunk/chunk_" + to_string(i) + ".csv";
        files[i].open(filename);
        if (files[i].is_open()) {
            string line;
            getline(files[i], line); // Пропуск заголовка
            if (getline(files[i], line)) {
                pq.push({parseCSV(line), i});
            }
        }
    }

    // 2. Пишем в итоговый файл
    ofstream outFile(output_filename);
    outFile << "Character_Name,Level,Win_Rate,Is_Banned,Last_Login\n";

    // 3. Главный цикл слияния
    while (!pq.empty()) {
        QueueNode best = pq.top();
        pq.pop();

        outFile << best.player.name << "," << best.player.level << ","
                << best.player.winrate << "," << (best.player.ban ? "True" : "False") << ","
                << best.player.lastlogin << "\n";

        string next_line;
        if (getline(files[best.file_index], next_line)) {
            pq.push({parseCSV(next_line), best.file_index});
        }
    }

    // 4. Закрываем и УДАЛЯЕМ чанки
    outFile.close();
    for (int i = 0; i < total_chunks; ++i) {
        files[i].close();
        string filename = "chunk/chunk_" + to_string(i) + ".csv";
        remove(filename.c_str()); 
    }
}

// === ГЛАВНАЯ ФУНКЦИЯ ===
// Добавили параметры для получения команд от интерфейса (argv)
int main(int argc, char* argv[]) {
    SetConsoleOutputCP(CP_UTF8);
    
    // Считываем режим сортировки, если он передан
    if (argc > 1) {
        string mode = argv[1];
        if (mode == "name") current_sort_mode = 2;
        else if (mode == "winrate") current_sort_mode = 3;
        else current_sort_mode = 1;
    }

    int time_start = clock();

    // === ЭТАП 1: РАЗБИЕНИЕ ===
    cout << "Этап 1: Читаем файл и нарезаем на чанки..." << endl;
    ifstream file("mmo_stats.csv");
    if (!file.is_open()) {
        cout << "Ошибка: не найден файл mmo_stats.csv!" << endl;
        return 1;
    }
    
    string line;
    getline(file, line); // Пропуск заголовка
    vector<Stats> chunk;
    int chunks_count = 0;
    
    while (getline(file, line)) {
        chunk.push_back(parseCSV(line));
        if (chunk.size() == 100000) {
            sort(chunk.begin(), chunk.end(), CustomSort);
            saveChunk(chunk, "chunk/chunk_" + to_string(chunks_count) + ".csv");
            chunk.clear();
            chunks_count++;
        }
    }
    if (!chunk.empty()) { // Хвост
        sort(chunk.begin(), chunk.end(), CustomSort);
        saveChunk(chunk, "chunk/chunk_" + to_string(chunks_count) + ".csv");
        chunks_count++;
    }
    file.close();

    // === ЭТАП 2: СЛИЯНИЕ ===
    cout << "Этап 2: Сливаем " << chunks_count << " файлов в один..." << endl;
    mergeChunks(chunks_count, "sorted_cpp.csv");

    int time_end = clock();
    cout << "ГОТОВО! Файл sorted_cpp.csv создан." << endl;
    cout << "Общее время: " << (time_end - time_start) / CLOCKS_PER_SEC << " секунд." << endl;

    return 0;
}