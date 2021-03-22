import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# paginate the questions on the trivia page

def paginate_questions(request, questions):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in questions]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # CORS(app) for all origins
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  
  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()
    categories_dictionary = {}
    for category in categories:
      categories_dictionary[category.id] = category.type

  # return 404 if no category is found
    if len(categories_dictionary) == 0:
      abort(404)

  # return data for categories
    return jsonify({
      'success': True,
      'categories': categories_dictionary,
      'total_categories': len(categories)
    })

  @app.route('/questions')
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)

    categories = Category.query.order_by(Category.id).all()
    categories_dictionary = {}
    for category in categories:
      categories_dictionary[category.id] = category.type

  # return 404 if no question is found
    if len(current_questions) == 0:
      abort(404)

  # return data for questions
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_paginated_questions': len(current_questions),
      'total_questions': len(Question.query.all()),
      'categories': categories_dictionary
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

  # return 404 if no question matches the ID
      if question is None:
        abort(404)

  # delete the question and format the paginated questions
      question.delete()
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)

  # return data for deleted question
      return jsonify({
        'success': True,
        'deleted': question.format(),
        'deleted_id': question_id,
        'questions': current_questions,
        'total_questions': len(questions)
      })

  # return 422 if any problem happens
    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

  # search for a term 
    try:
        search_term = body.get('searchTerm', None)
        if search_term:
          questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
          current_questions = paginate_questions(request, questions)              
  
  # return data for searched question
          return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': len(questions),
              'search_term': search_term
      })

  # load new data
        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            question = Question(question=new_question, 
                                answer=new_answer, 
                                category=new_category, 
                                difficulty=new_difficulty)
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            
            # return data for new question
            return jsonify({
                'question': new_question,
                'answer': new_answer,
                'category': new_category,
                'difficulty': new_difficulty,
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

  # return 422 if any problem happens
    except:
      abort(422)

  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
      category = Category.query.filter_by(id=category_id).one_or_none()

  # return 404 if no category matches the ID
      if category is None:
        abort(404)
    
      questions = Question.query.filter_by(category=category.id).all()
      current_questions = paginate_questions(request, questions)

  # return data for questions
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(current_questions),
        'selected_category': category.type
      })


  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()

    # take previous question parameters
    category = body.get('quiz_category', None)
    category_id = category['id']
    previous_questions = body.get('previous_questions', None)

    # return 400 if no  category or question is found
    if (category is None) or (previous_questions is None):
      abort(400)

    # if no category is selected then query all questions
    if category_id == 0:
      questions = Question.query.order_by(Question.id).all()

    # if specific category is selected then only select the questions from that category
    else:
      questions = Question.query.filter_by(category=category_id).all()

    # create list of new questions to be randomised
    new_user_questions = []

    # if no question has not been shown to participant before, use all questions
    for question in questions:
      if question.id not in previous_questions:
        new_user_questions.append(question)

    if new_user_questions == []:
      formatted_question = 0

    # if questions have been shown before, randomise the new questions
    else:
      question = random.choice(new_user_questions)
      formatted_question = question.format()
      previous_questions.append(formatted_question)
    
    # return data for new question
    try:
      return jsonify({
        'success': True,
        'question': formatted_question
      })

    except:
      abort(422)

# error handling

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
      "success":False,
      "error":400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
      "success":False,
      "error":404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
      "success":False,
      "error":405,
      "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
      "success":False,
      "error":422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
      "success":False,
      "error":500,
      "message": "internal server error"
      }), 500  

  return app
