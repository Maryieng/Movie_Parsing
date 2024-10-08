from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.models import Movie, SessionLocal
from app.scraper import scrape_movies

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Загрузка фильмов
@app.post("/load_movies")
def load_movies(db: Session = Depends(get_db)):
    movies = scrape_movies()
    for movie_data in movies:
        movie = Movie(
            title=movie_data['title'],
            description=movie_data['description'],
            imdb_rating=movie_data['imdb_rating'],
            year=movie_data['year'],
            poster_url=movie_data['poster_url'],
            local_image_path=movie_data['local_image_path']
        )
        db.add(movie)
    db.commit()
    return {"message": "Фильмы успешно загружены"}

# Получение всех фильмов
@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return [
        {
            "title": movie.title,
            "description": movie.description,
            "imdb_rating": movie.imdb_rating,
            "year": movie.year,
            "poster_url": movie.poster_url,
            "local_image_path": movie.local_image_path,
        }
        for movie in movies
    ]

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Фильмы</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
            <link rel="stylesheet" href="static/css/style.css">
        </head>
        <body>
            <div class="container">
                <h1>Фильмы</h1>
                <button id="load-movies" class="btn btn-primary">Загрузить фильмы</button>
                <table id="movie-table" class="table table-striped">
                    <thead>
                        <tr>
                            <th>Название</th>
                            <th>Описание</th>
                            <th>Рейтинг IMDb</th>
                            <th>Год</th>
                            <th>Постер</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp+G7niu735Sk7lN" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqXnG+pc0ilTghWdg" crossorigin="anonymous"></script>
            <script src="static/js/app.js"></script>
        </body>
        </html>
    """

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
