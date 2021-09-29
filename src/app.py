import os
import json
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import exc
from .database.models import setup_db, Actor, Movie


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    CORS(app)
    db = setup_db(app)
    migrate = Migrate(app, db)

    '''
    Actor Endpoints
    '''
    # Retrive Actor List
    @app.route('/actors', methods=['GET'])
    def retrieve_actors_list():
        try:
            actors = Actor.query.all()
            formatted_actors = [actor.format() for actor in actors]

            return jsonify(formatted_actors)
        except exc.SQLAlchemyError:
            abort(400)

    # Create Actor
    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        # TODO: Add checks for validity of input

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                "success": True,
                "status_code": 200,
                "created_id": actor.id
            })
        except exc.SQLAlchemyError:
            abort(400)

    # Retrive Actor
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    def retrive_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(404)

            return jsonify({
                "success": True,
                "status_code": 200,
                "actor": actor.format()
            })
        except exc.SQLAlchemyError:
            abort(400)

    # Update Actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(404)

            body = request.get_json()
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            # TODO: Add checks for validity of input

            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "actor": actor.format()
            })
        except exc.SQLAlchemyError:
            abort(400)

    # Delete Actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(404)

            actor.delete()
            return jsonify({
                "success": True,
                "status_code": 200,
                "deleted_id": actor.id
            })
        except exc.SQLAlchemyError:
            abort(400)

    '''
    Movie Endpoints
    '''
    # Retrieve Movie List
    @app.route('/movies')
    def retrieve_movies_list():
        try:
            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]

            return jsonify(formatted_movies)
        except exc.SQLAlchemyError:
            abort(400)

    # Create Movie
    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()

        title = body.get('title')
        release_year = body.get('release_year')

        # TODO: Add checks for validity of input

        try:
            movie = Movie(title=title, release_year=release_year)
            movie.insert()

            return jsonify({
                "success": True,
                "status_code": 200,
                "created_id": movie.id
            })
        except exc.SQLAlchemyError:
            abort(400)

    # Retrieve Movie
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    def retrive_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            return jsonify({
                "success": True,
                "status_code": 200,
                "movie": movie.format()
            })
        except exc.SQLAlchemyError:
            abort(400)

    # Update Movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            body = request.get_json()
            title = body.get('title')
            release_year = body.get('release_year')

            # TODO: Add checks for validity of input

            if title is not None:
                movie.title = title
            if release_year is not None:
                movie.release_year = release_year

            movie.update()

            return jsonify({
                "success": True,
                "status_code": 200,
                "movie": movie.format()
            })
        except exc.SQLAlchemyError:
            abort(400)

    # Delete Movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            movie.delete()
            return jsonify({
                "success": True,
                "status_code": 200,
                "deleted_id": movie.id
            })
        except exc.SQLAlchemyError:
            abort(400)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
