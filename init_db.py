import sqlite3

def init_db():
    con = sqlite3.connect('base.db')
    cur = con.cursor()

    # Создание таблицы для фильмов
    cur.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        commentary TEXT,
        rating TEXT,
        url_image TEXT NOT NULL,
        age_restriction TEXT NOT NULL
    )''')

    # Создание таблицы для детских мероприятий
    cur.execute('''CREATE TABLE IF NOT EXISTS childrens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        commentary TEXT,
        rating TEXT,
        url_image TEXT NOT NULL,
        age_restriction TEXT NOT NULL
    )''')

    # Создание таблицы для концертов
    cur.execute('''CREATE TABLE IF NOT EXISTS concerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        commentary TEXT,
        rating TEXT,
        url_image TEXT NOT NULL,
        age_restriction TEXT NOT NULL
    )''')

    # Создание таблицы для встреч
    cur.execute('''CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        commentary TEXT,
        rating TEXT,
        url_image TEXT NOT NULL,
        age_restriction TEXT NOT NULL
    )''')

    # Создание таблицы для театра
    cur.execute('''CREATE TABLE IF NOT EXISTS theatre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        commentary TEXT,
        rating TEXT,
        url_image TEXT NOT NULL,
        age_restriction TEXT NOT NULL
    )''')

    con.commit()
    con.close()

if __name__ == '__main__':
    init_db()
    print("База данных успешно инициализирована!") 