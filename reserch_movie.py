import requests
import dotenv
from pprint import pprint
dotenv.load_dotenv()

api_key = dotenv.get_key(".env", "API_KEY")
access_key = dotenv.get_key(".env", "ACCESS_KEY")


def start():
    url = "https://api.themoviedb.org/3/authentication"
    headers = {"accept": "application/json", "Authorization": access_key}
    response = requests.get(url, headers=headers)
    print(response.text)

start()


# title = input("Введите название фильма: ")
def new_movie(title):
    list = []
    # Получаем название фильма от пользователя

    # Формируем URL с параметром запроса
    url = f"https://api.themoviedb.org/3/search/movie"
    # Заголовки для авторизации
    headers = {"accept": "application/json", "Authorization": access_key}
    # Параметры запроса
    params = {"query": title,}
    # Выполняем запрос к API с методом GET
    response = requests.get(url, headers=headers, params=params)
    all_movies = response.json()

    # Проверяем, успешно ли выполнен запрос
    if response.status_code == 200:
        print(response.json())  # Выводим данные в формате JSON
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
    if all_movies:
        for movie in all_movies["results"]:
            id = movie["id"]
            title = movie["title"]
            year = movie["release_date"][:4]
            discription = movie["overview"]
            rating = movie["vote_average"]
            image = f"https://image.tmdb.org/t/p/w500/{movie["poster_path"]}"

            movie_data = {
                "id": id,
                "title": title,
                "year": year,
                "description": discription,
                "rating": rating,
                "image": image
            }

            list.append(movie_data)
    return list

def get_movie(id):
    url = f"https://api.themoviedb.org/3/movie/{id}"
    headers = {"accept": "application/json", "Authorization": access_key}
    response = requests.get(url, headers=headers)
    movie = response.json()
    movie = {
        "id": movie["id"],
        "title": movie["title"],
        "year": movie["release_date"][:4],
        "description": movie["overview"],
        "rating": movie["vote_average"],
        "image": f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
    }
    return movie

# movie = get_movie(555879)
# print(movie)



