import requests
from bs4 import BeautifulSoup
import os

def scrape_movies():
    url = "https://www.kinopoisk.ru/lists/movies/popular-films/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    movies = []
    if not os.path.exists('static/images'):
        os.makedirs('static/images')

    for movie_div in soup.find_all('div', class_='styles_mainItem__1z6Zq'):
        title = movie_div.find('a', class_='styles_title__57B6F').text
        description = movie_div.find('div', class_='styles_description__2InUX').text.strip() if movie_div.find('div', class_='styles_description__2InUX') else "Нет описания"
        imdb_rating = movie_div.find('span', class_='styles_ratingValue__3_5hP').text.strip()
        year = movie_div.find('span', class_='styles_year__28Z_c').text.strip()
        poster_url = movie_div.find('img', class_='styles_image__1e92Z').get('src')

    # Загрузка изображения
        local_image_path = f'static/images/{title.replace(" ", "_")}.jpg'
        with open(local_image_path, 'wb') as img_file:
          img_data = requests.get(poster_url).content
          img_file.write(img_data)

        movie_data = {
            'title': title,
            'description': description,
            'imdb_rating': float(imdb_rating),
            'year': int(year),
            'poster_url': poster_url,
            'local_image_path': local_image_path,
        }
        movies.append(movie_data)
    return movies
