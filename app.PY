from flask import Flask, jsonify, request
from models import db, Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return "Welcome to Mini Movie Rental API"

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    if movie:
        return jsonify(movie.to_dict()), 200
    return jsonify({"message": "Movie not found"}), 404

@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        genre=data['genre'],
        available=data.get('available', True)
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict()), 201

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    data = request.get_json()
    movie.title = data.get('title', movie.title)
    movie.genre = data.get('genre', movie.genre)
    movie.available = data.get('available', movie.available)
    db.session.commit()
    return jsonify(movie.to_dict()), 200

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
