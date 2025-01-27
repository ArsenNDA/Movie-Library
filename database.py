import sqlite3

DB_NAME = "movies.db"


# Инициализация базы данных (создание таблицы, если её нет)
def init_db():
    """Создаёт таблицу, если она не существует"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            rating INTEGER NOT NULL,
            ranking INTEGER ,
            review TEXT ,
            img_url TEXT NOT NULL
        );
    ''')
    connection.commit()
    connection.close()


# Добавление книги
def add_movie(title, year, description, rating,  img_url, ranking=None, review=None):
    """Добавляет книгу в базу данных"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO movie (title, year, description, rating, ranking, review, img_url)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        ''', (title, year, description, rating, ranking, review, img_url))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка добавления книги: {e}")
    finally:
        connection.close()


# Изменение книги
def update_movie(movie_id, new_ranking=None, new_review=None):
    """
    Обновляет информацию о книге.
    Можно передать только те параметры, которые нужно изменить.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    try:
        if new_ranking is not None:
            cursor.execute('''
                UPDATE movie
                SET ranking = ?
                WHERE id = ?;
            ''', (new_ranking, movie_id))
        if new_review is not None:
            cursor.execute('''
                UPDATE movie
                SET review = ?
                WHERE id = ?;
            ''', (new_review, movie_id))
        connection.commit()
    except sqlite3.IntegrityError as e:
        print(f"Ошибка изменения книги: {e}")
    finally:
        connection.close()


# Удаление книги
def delete_movie(movie_id):
    """Удаляет книгу по её id"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM movie
        WHERE id = ?;
    ''', (movie_id,))
    connection.commit()
    connection.close()


# Получение всех книг
def get_all_movies():
    """Возвращает все книги из базы данных в виде списка"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movie;')
    movies = cursor.fetchall()
    connection.close()
    return movies


# Получение книги по ID
def get_movie_by_id(movie_id):
    """Возвращает информацию о книге по её ID или None, если книга не найдена."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row  # Возвращать данные в виде словарей
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movie WHERE id = ?;', (movie_id,))
    movie = cursor.fetchone()
    connection.close()

    if movie is None:
        print(f"Movie with ID {movie_id} not found.")
        return None

    # Преобразование данных из sqlite3.Row в обычный словарь
    movie_dict = {
        "id": movie["id"],
        "title": movie["title"],
        "year": movie["year"],
        "description": movie["description"],
        "rating": movie["rating"],
        "ranking": movie["ranking"] if movie["ranking"] is not None else None,
        "review": movie["review"] if movie["review"] is not None else None,
        "img_url": movie["img_url"],
    }
    print(movie_dict)
    return movie_dict

get_movie_by_id(3)
