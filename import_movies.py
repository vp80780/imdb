import os
import simplejson


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'imdb.settings')

    import django
    import json
    django.setup()

    from django.db import connection
    from apps.movies.models import Movies, Genre

    file = open('Task_1_data.json', 'r')
    movies = simplejson.load(file)
    for single_movie in movies:
        movie = Movies.objects.create(name=single_movie['name'],
                                      director=single_movie['director'],
                                      imdb_score=single_movie['imdb_score'],
                                       popularity=single_movie['99popularity'])

        for genre in single_movie['genre']:
            genre_obj = Genre.objects.filter(genre=genre.strip())
            if genre_obj:
                movie.genre.add(genre_obj[0])
                movie.save()
            else:
                genre_obj = Genre.objects.create(genre=genre.strip())
                genre_obj.save()
                movie.genre.add(genre_obj)
                movie.save()

    print('Movies has been stored successfully...')
