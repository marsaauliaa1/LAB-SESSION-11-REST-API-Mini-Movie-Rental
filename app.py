# app.py

from flask import Flask, jsonify, request
from movies import Movie

app = Flask(__name__)

# Dummy data awal (opsional)
Movie.add_movie("Inception", "Sci-Fi")
Movie.add_movie("The Godfather", "Crime")

@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify(Movie.get_all()), 200

@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = Movie.get_by_id(movie_id)
    if movie:
        return jsonify(movie.to_dict()), 200
    return jsonify({"message": "Movie not found"}), 404

@app.route("/movies", methods=["POST"])
def create_movie():
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "genre")):
        return jsonify({"message": "Invalid data"}), 400
    movie = Movie.add_movie(data["title"], data["genre"], data.get("available", True))
    return jsonify(movie.to_dict()), 201

@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    data = request.get_json()
    movie = Movie.update_movie(
        movie_id,
        title=data.get("title"),
        genre=data.get("genre"),
        available=data.get("available")
    )
    if movie:
        return jsonify(movie.to_dict()), 200
    return jsonify({"message": "Movie not found"}), 404

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    success = Movie.delete_movie(movie_id)
    if success:
        return jsonify({"message": "Movie deleted"}), 200
    return jsonify({"message": "Movie not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
