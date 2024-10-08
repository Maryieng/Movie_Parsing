$(document).ready(function() {
    $("#load-movies").click(function() {
        $.ajax({
            url: "/load_movies",
            type: "POST",
            success: function() {
                // Обновление таблицы после загрузки фильмов
                loadMovies();
            },
            error: function() {
                alert("Ошибка при загрузке фильмов");
            }
        });
    });

    // Функция для загрузки фильмов
    function loadMovies() {
        $.ajax({
            url: "/movies",
            type: "GET",
            success: function(movies) {
                $("#movie-table tbody").empty(); // Очистка таблицы
                movies.forEach(movie => {
                    $("#movie-table tbody").append(`
                        <tr>
                            <td>${movie.title}</td>
                            <td>${movie.description}</td>
                            <td>${movie.imdb_rating}</td>
                            <td>${movie.year}</td>
                            <td><img src="${movie.local_image_path}" width="100" height="150"></td>
                        </tr>
                    `);
                });
            },
            error: function() {
                alert("Ошибка при получении фильмов");
            }
        });
    }

    // Загрузка начальных данных о фильмах
    loadMovies();
});