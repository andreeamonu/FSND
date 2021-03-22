import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

## ROUTES

'''
Retrieve all drinks
'''

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    # create short drink
    drinks_short = [drink.short() for drink in drinks]

    # return 404 if no drink is found
    if len(drinks) == 0:
        abort(404)

    # return data for drinks
    return jsonify({
        'success': True,
        'drinks': drinks_short
    }), 200

'''
Retrieve detailed drinks
'''
@app.route('/drinks-detail')
@requires_auth("get:drinks-detail")
def get_drinks_detail(jwt):
    drinks = Drink.query.all()

    # create long drink
    drinks_long = [drink.long() for drink in drinks]

    # return 404 if no drink is found
    if len(drinks) == 0:
        abort(404)

    # return data for drinks
    return jsonify({
        'success': True,
        'drinks': drinks_long
    }), 200

'''
Create drinks
'''

@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def post_drinks(jwt):

    # get drink information
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    # update database with new drink details
    drink = Drink(title=new_title, 
                  recipe=json.dumps(new_recipe))
    try:
        drink.insert()
        
        # return data for new drink
        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200

    # return 422 if any problem happens
    except Exception as e: 
        print(e)

'''
Update drink details
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def update_drink(jwt, drink_id):
    # get drink information
    body = request.get_json()
    updated_title = body.get('title', None)
    updated_recipe = body.get('recipe', None)

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    # return 404 if no drink matches the ID
        if drink is None:
            abort(404)

    # update the drink
        if updated_title is not None:
            drink.title = updated_title
        if updated_recipe is not None:
            drink.recipe = json.dumps(updated_recipe)
        drink.update()


    # return data for deleted drink
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

# return 422 if any problem happens
    except Exception as e: 
        print(e)

'''
Delete drink
'''

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth("delete:drinks")
def delete_drink(jwt, drink_id):

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    # return 404 if no drink matches the ID
    if drink is None:
        abort(404)

    # delete the drink
    try:
        drink.delete()

    # return data for deleted drink
        return jsonify({
            'success': True,
            'delete': drink_id
        }), 200

    # return 422 if any problem happens
    except Exception as e: 
        print(e)

## Error Handling

'''
User Error
'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success":False,
                    "error":400,
                    "message": "bad request"
                    }), 400

'''
Unauthorised Error
'''

@app.errorhandler(401)
def not_found(error):
      return jsonify({
                    "success":False,
                    "error":401,
                    "message": "unauthorized"
                    }), 401

'''
Not found Error
'''

@app.errorhandler(404)
def not_found(error):
      return jsonify({
                    "success":False,
                    "error":404,
                    "message": "resource not found"
                    }), 404

'''
Method requested Error
'''

@app.errorhandler(405)
def not_allowed(error):
      return jsonify({
                    "success":False,
                    "error":405,
                    "message": "method not allowed"
                    }), 405

'''
Unprocessable Request
'''

@app.errorhandler(422)
def unprocessable(error):
      return jsonify({
                    "success":False,
                    "error":422,
                    "message": "unprocessable"
                    }), 422

'''
Server Error
'''

@app.errorhandler(500)
def internal_server_error(error):
      return jsonify({
                    "success":False,
                    "error":500,
                    "message": "internal server error"
                    }), 500  


'''
Authorisation Error
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Receive the raised authorization error and propagates it as response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response