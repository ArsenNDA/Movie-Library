import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from database import init_db, add_movie, update_movie, delete_movie, get_all_movies, get_movie_by_id
from reserch_movie import new_movie, get_movie
import dotenv
dotenv.load_dotenv()
app_secret_key = os.getenv("APP_CONTENT")

app = Flask(__name__)
app.config['SECRET_KEY'] = app_secret_key
init_db()


@app.route("/")
def home():
    movies = get_all_movies()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    title = request.form.get("title")
    if title:
        return redirect(url_for("select", title=title))
    return render_template("add.html",)


@app.route("/select", methods=["GET", "POST"])
def select():
    # Получаем title из строки запроса
    title = request.args.get("title")
    movies = new_movie(title)

    # Если указан id фильма, перенаправить на маршрут добавления фильма
    movie_id = request.args.get("id")
    if movie_id:
        return redirect(url_for("add_movie", id=int(movie_id)))

    return render_template("select.html", movies=movies)




@app.route('/add_movie/<int:id>', methods=['GET', 'POST'])
def add_movie_route(id):  # Изменено имя функции маршрута
    # Получение информации о фильме по id
    movie = get_movie(id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Извлечение данных о фильме
    title = movie['title']
    year = movie['year']
    description = movie['description']
    rating = movie['rating']
    img_url = movie['image']

    ranking = request.form.get("ranking")
    review = request.form.get("review")

    if request.method == 'POST':
        # Вызов функции добавления фильма из базы данных
        add_movie(title=title, year=year, description=description, rating=rating, ranking=ranking, review=review,
                  img_url=img_url)
        print("Movie added successfully!")
        return redirect(url_for("home"))

    # Проверка наличия всех параметров
    if not all([title, year, description, rating, img_url]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Рендеринг шаблона
    return render_template("add_movie.html", title=title, year=year, description=description, rating=rating,
                           img_url=img_url)



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    movie = get_movie_by_id(id)
    # Инициализация переменных значениями из базы данных (метод GET)
    title = movie['id']
    year = movie['year']
    description = movie['description']
    rating = movie['rating']
    ranking = movie['ranking']
    review = movie['review']
    img_url = movie['img_url']

    if request.method == "POST":
        # Обновляем данные переменных из формы (метод POST)
        ranking = request.form.get("ranking")
        review = request.form.get("review")

        # Обновление фильма в базе данных
        update_movie(
            movie_id=id,
            new_ranking=ranking,
            new_review=review,
        )
        return redirect(url_for("home"))
    return render_template("edit.html", title=title, year=year, description=description, rating=rating, ranking=ranking, review=review, img_url=img_url)

@app.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    """Удаляет книгу по её ID"""
    delete_movie(id)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)