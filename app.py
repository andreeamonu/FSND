import os
import json
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors, movie_actors
from auth import requires_auth, AuthError

def create_app(test_config=None):

    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # CORS Headers
    @app.after_request
    def after_request(response):

        # Allow requests headers ( Content-Type, Authorization)
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,true')

        # Allow specific requests methods (GET, POST, PATCH, DELETE, OPTIONS)
        response.headers.add('Access-Control-Allow-Methods',
                                'GET,PATCH,POST,DELETE,OPTIONS')
        return response

# Endpoints

#----------------------------------------------------------------------------#
# Movies
#----------------------------------------------------------------------------#

# Retrieve movies

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movies.query.order_by(Movies.id).all()

        movies = [movie.format() for movie in movies]

        # return 404 if no movie is found
        if len(movies) == 0:
            abort(404)

        # return data for movies
        return jsonify({
            'success': True,
            'movies': movies,
            'number_of_movies': len(Movies.query.all())
        }), 200

    # Create movies

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movies")
    def post_movies(payload):

        # get movies information
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        # update database with new movie details
        movie = Movies(title=new_title, 
                    release_date=new_release_date)
        try:
            movie.insert()
            
            # return data for new movie
            return jsonify({
                'success': True,
                'movie': movie.format(),
                'number_of_movies': len(Movies.query.all())
            }), 200

        # return 422 if any problem happens
        except Exception as e: 
            print(e)

    # Update movie details

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movie(payload, movie_id):
        # get movie information
        body = request.get_json()
        updated_title = body.get('title', None)
        updated_release_date = body.get('release_date', None)

        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        # return 404 if no movie matches the ID
            if movie is None:
                abort(404)

        # update the movie
            if updated_title is not None:
                movie.title = updated_title
            if updated_release_date is not None:
                movie.release_date = updated_release_date
            movie.update()

        # return data for deleted movie
            return jsonify({
                'success': True,
                'movies': [movie.format()],
                'number_of_movies': len(Movies.query.all())
            }), 200

    # return 422 if any problem happens
        except Exception as e: 
            print(e)

    # Delete movie

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):

        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        # return 404 if no movie matches the ID
        if movie is None:
            abort(404)

        # delete the movie
        try:
            movie.delete()

        # return data for deleted movie
            return jsonify({
                'success': True,
                'delete': movie_id,
                'number_of_movies': len(Movies.query.all())
            }), 200

        # return 422 if any problem happens
        except Exception as e: 
            print(e)

#----------------------------------------------------------------------------#
# Actors
#----------------------------------------------------------------------------#

# Retrieve actors

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.order_by(Actors.id).all()

        actors = [actor.format() for actor in actors]

        # return 404 if no actor is found
        if len(actors) == 0:
            abort(404)

        # return data for actors
        return jsonify({
            'success': True,
            'actors': actors,
            'number_of_actors': len(Actors.query.all())
        }), 200

    # Create actors

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actors")
    def post_actors(payload):

        # get actor information
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        # update database with new actor details
        actor = Actors(name=new_name,
                    age=new_age,
                    gender=new_gender)
        try:
            actor.insert()
            
            # return data for new actor
            return jsonify({
                'success': True,
                'actor': actor.format(),
                'number_of_actors': len(Actors.query.all())
            }), 200

        # return 422 if any problem happens
        except Exception as e: 
            print(e)

    # Update actor details

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actor(payload, actor_id):
        # get actor information
        body = request.get_json()
        updated_name = body.get('name', None)
        updated_age = body.get('age', None)
        updated_gender = body.get('gender', None)

        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        # return 404 if no actor matches the ID
            if actor is None:
                abort(404)

        # update the actor
            if updated_name is not None:
                actor.name = updated_name
            if updated_age is not None:
                actor.age = updated_age
            if updated_gender is not None:
                actor.gender = updated_gender
            actor.update()


        # return data for deleted actor
            return jsonify({
                'success': True,
                'actors': [actor.format()],
                'number_of_actors': len(Actors.query.all())
            }), 200

    # return 422 if any problem happens
        except Exception as e: 
            print(e)

    # Delete actor

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):

        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        # return 404 if no actor matches the ID
        if actor is None:
            abort(404)

        # delete the actor
        try:
            actor.delete()

        # return data for deleted actor
            return jsonify({
                'success': True,
                'delete': actor_id,
                'number_of_actors': len(Actors.query.all())
            }), 200

        # return 422 if any problem happens
        except Exception as e: 
            print(e)

#----------------------------------------------------------------------------#
# Errors
#----------------------------------------------------------------------------#

# User error

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success":False,
                        "error":400,
                        "message": "bad request"
                        }), 400

    # Unauthorised Error

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
                        "success":False,
                        "error":401,
                        "message": "unauthorized"
                        }), 401

    # Not found Error

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success":False,
                        "error":404,
                        "message": "resource not found"
                        }), 404

    # Method requested Error

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
                        "success":False,
                        "error":405,
                        "message": "method not allowed"
                        }), 405

    # Unprocessable Request

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success":False,
                        "error":422,
                        "message": "unprocessable"
                        }), 422

    # Server Error

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
                        "success":False,
                        "error":500,
                        "message": "internal server error"
                        }), 500  


    # Authorisation Error

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app

#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)