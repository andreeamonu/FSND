# Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the casting_agency.psql file provided. Just run:
```bash
createuser local-admin
dropdb casting
createdb casting
psql casting < casting_agency.psql
```

## Running the server locally

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app && export FSK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory to find the application. 

## Testing
To run the tests that are looking both at happy path scenarios as well as unhappy paths, run:
```
dropdb casting_test
createdb casting_test
psql casting_test < casting_agency.psql
python test_app.py
```
Please Note: You will have to generate new tokens and replace them in the constants at the top of the test file in order for the tests to run properly.

## API Reference

### Getting Started

- The Casting Agency API is organised around REST. The API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.
- Base URL: https://fsnd-andreea-casting-agency.herokuapp.com
- You can run local requests also using Postman or curl. For Postman collection - please find andreea-casting.postman_collection. For local requests use http://127.0.0.1:5000/, accompanied by a working token
- Authentication: This version of the application requires authentication.

### Error Handling

Errors are returned as JSON objecrs in the following format:
```
{
    "success": False,
    "error": 400,
    "message: "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

### Roles and Permissions

The Casting Agency API currently has 3 roles with the following permissions:
- Casting Assistant
  - `get:movies`
  - `get:actors`
- Casting Director
  - `get:movies`
  - `get:actors`
  - `add:actors`
  - `delete:actors`
  - `patch:movies`
  - `patch:actors`
- Executive Producer
  - `get:movies`
  - `get:actors`
  - `add:actors`
  - `delete:actors`
  - `patch:movies`
  - `patch:actors`
  - `add:movies`
  - `delete:movies`

### Endpoints

#### GET /movies
- General:
    - Returns a list of all movies, success value and total number of movies assuming you have the permission.
    - Results show all available movies.
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
#### GET /actors
- General:
    - Returns a list of  question objects, categories available, success value, number of paginated questions and total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_paginated_questions": 10, 
  "total_questions": 19
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes a question based on question ID if it exists.
    - Results contain the details of question deleted (answer, category, difficulty, id, question), success value, total questions, and question list based on current page number to update the frontend. 
```
{
  "deleted": {
    "answer": "Armando Dippet", 
    "category": 5, 
    "difficulty": 4, 
    "id": 24, 
    "question": "Who was the Hogwarts headmaster right before Dumbledore?"
  }, 
  "deleted_id": 24, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```
#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and category.
    - Results contain the new question contents (answer, category, id, difficulty, question), success value, total number of questions and question list based on current page number to update the frontend.
```
{
  "answer": "Gregor Mendel", 
  "category": 1, 
  "created": 26, 
  "difficulty": 2, 
  "question": "Who is considered the founder of the modern study of genetics?", 
  "questions": [
    {
      "answer": "Gregor Mendel", 
      "category": 1, 
      "difficulty": 2, 
      "id": 26, 
      "question": "Who is considered the founder of the modern study of genetics?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```
#### POST /questions with searchTerm
- General:
    - Returns questions based on the search term used by the customer.
    - The search is only applied to the question.
    - Results contain the questions found, answer, category, difficulty and id, are paginated in sets, have success value, number of questions that contain the search term and the search term that has been used.
```
{
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "search_term": "Gogh", 
  "success": true, 
  "total_questions": 1
}
```
#### GET /categories/{category_id}/questions
- General:
    - Returns questions that are in the selected category.
    - Results contain the question, answer, category, difficulty and id, paginated in sets, success value, number of questions that are part of the category and the category selected.
    - Category IDs can be located at the GET /category endpoint.
```
{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "selected_category": "Science", 
  "success": true, 
  "total_questions": 3
}
```
#### POST /quizzes
- General:
    - Returns a random question from the list of questions that belong in a chosen category.
    - Results contain the question, answer, category, difficulty and id, and success value.
```
{
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }, 
  "success": true
}
```

## Deployment N/A

## Authors
Andreea Monu 

## Acknowledgements 
The awesome team at Udacity teaching us new concepts and helping me become a full stack developer!