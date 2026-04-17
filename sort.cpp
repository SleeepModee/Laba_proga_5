#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <queue>
#include <sstream>

using namespace std;

// Структура для хранения одной записи из нашего CSV
struct PlayerRecord {
    string name;
    int level;
    double win_rate;
    bool is_banned;
    string last_login;
};

// Функция для парсинга одной строки CSV в нашу структуру
PlayerRecord parseCSVLine(const string& line) {
    PlayerRecord record;
    stringstream ss(line);
    string token;

    // Парсим Character_Name
    getline(ss, record.name, ',');
    
    // Парсим Level
    getline(ss, token, ',');
    record.level = stoi(token);
    
    // Парсим Win_Rate
    getline(ss, token, ',');
    record.win_rate = stod(token);
    
    // Парсим Is_Banned (в Python мы писали True/False)
    getline(ss, token, ',');
    record.is_banned = (token == "True");
    
    // Парсим Last_Login
    getline(ss, record.last_login, ',');

    return record;
}

int main() {
    cout << "C++ модуль сортировки запущен." << endl;
    
    // Для проверки работы парсера (потом мы это удалим)
    string test_line = "ShadowSlayer,85,54.2,False,2023-11-01";
    PlayerRecord test_record = parseCSVLine(test_line);
    
    cout << "Тест парсера: Имя=" << test_record.name 
         << ", Уровень=" << test_record.level << endl;

    return 0;
}