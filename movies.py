# movies.py

class Movie:
    _movies = []
    _id_counter = 1

    def __init__(self, title, genre, available=True):
        self.id = Movie._id_counter
        self.title = title
        self.genre = genre
        self.available = available
        Movie._id_counter += 1

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "available": self.available
        }

    @classmethod
    def get_all(cls):
        return [movie.to_dict() for movie in cls._movies]

    @classmethod
    def get_by_id(cls, movie_id):
        for movie in cls._movies:
            if movie.id == movie_id:
                return movie
        return None

    @classmethod
    def add_movie(cls, title, genre, available=True):
        movie = Movie(title, genre, available)
        cls._movies.append(movie)
        return movie

    @classmethod
    def update_movie(cls, movie_id, title=None, genre=None, available=None):
        movie = cls.get_by_id(movie_id)
        if movie:
            if title is not None:
                movie.title = title
            if genre is not None:
                movie.genre = genre
            if available is not None:
                movie.available = available
            return movie
        return None

    @classmethod
    def delete_movie(cls, movie_id):
        movie = cls.get_by_id(movie_id)
        if movie:
            cls._movies.remove(movie)
            return True
        return False
