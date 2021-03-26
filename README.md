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
  - `post:actors`
  - `delete:actors`
  - `patch:movies`
  - `patch:actors`
- Executive Producer
  - `get:movies`
  - `get:actors`
  - `post:actors`
  - `delete:actors`
  - `patch:movies`
  - `patch:actors`
  - `post:movies`
  - `delete:movies`

### Endpoints

#### GET /movies
- General:
    - Returns a list of all movies, success value and total number of movies assuming you have the correct permission set.
    - Results show all available movies.
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 26 Jul 1991 00:00:00 GMT",
            "title": "Edward Scissorhands"
        },
        {
            "id": 2,
            "release_date": "Wed, 23 Sep 2020 00:00:00 GMT",
            "title": "Enola Holmes"
        },
        {
            "id": 3,
            "release_date": "Fri, 06 Feb 2009 00:00:00 GMT",
            "title": "The Curious Case of Benjamin Button"
        },
        {
            "id": 4,
            "release_date": "Mon, 18 Jun 2018 00:00:00 GMT",
            "title": "Ocean's Eight"
        },
        {
            "id": 5,
            "release_date": "Fri, 31 Oct 2014 00:00:00 GMT",
            "title": "Nightcrawler"
        },
        {
            "id": 6,
            "release_date": "Thu, 02 Oct 2014 00:00:00 GMT",
            "title": "Gone Girl"
        }
    ],
    "number_of_movies": 6,
    "success": true
}
```
#### POST /movies
- General:
    - Creates a new movie using the submitted title and release_date.
    - Results contain the new movie contents (id, release_date, title), success value, total number of movies
```
{
    "movies": {
        "id": 7,
        "release_date": "Fri, 20 Jul 2010 00:00:00 GMT",
        "title": "Inception"
    },
    "number_of_movies": 7,
    "success": true
}
```
#### PATCH /movies{movie_id}
- General:
    - Updates a movie in case values are wrong or they need to be updated.
    - Results contain the updated movie contents (id, release_date, title) and success value.
```
{
    "movies": [
        {
            "id": 7,
            "release_date": "Fri, 16 Jul 2010 00:00:00 GMT",
            "title": "\"Inception\""
        }
    ],
    "success": true
}
```

#### DELETE /movies/{movie_id}
- General:
    - Deletes a movie based on movie ID if it exists.
    - Results contain the id of the movie deleted, the release_date, title and success. 
```
{
    "movie": [
        {
            "id": 1,
            "release_date": "Fri, 26 Jul 1991 00:00:00 GMT",
            "title": "Edward Scissorhands"
        }
    ],
    "success": true
}
```

#### GET /actors
- General:
    - Returns a list of all actors, success value and total number of actors assuming you have the correct permission set.
    - Results show all available actors.
```
{
    "actors": [
        {
            "age": 51,
            "gender": "Female",
            "id": 1,
            "name": "Cate Blanchett"
        },
        {
            "age": 57,
            "gender": "Male",
            "id": 2,
            "name": "Brad Pitt"
        },
        {
            "age": 57,
            "gender": "Male",
            "id": 3,
            "name": "Johnny Depp"
        },
        {
            "age": 40,
            "gender": "Male",
            "id": 4,
            "name": "Jake Gyllenhaal"
        },
        {
            "age": 17,
            "gender": "Female",
            "id": 5,
            "name": "Millie Bobby Brown"
        },
        {
            "age": 48,
            "gender": "Male",
            "id": 6,
            "name": "Ben Affleck"
        }
    ],
    "number_of_actors": 6,
    "success": true
}
```
#### POST /actors
- General:
    - Creates a new actor using the submitted age, gender and name.
    - Results contain the new actor contents (age, gender, id, name), success value, total number of actors

```
{
    "actors": {
        "age": 45,
        "gender": "Female",
        "id": 7,
        "name": "Marion Cotillard"
    },
    "number_of_actors": 7,
    "success": true
}
```
#### PATCH /actors/{actor_id}
- General:
    - Updates an actor in case values are wrong or they need to be updated.
    - Results contain the updated actor contents (age, gender, id, name), success value, total number of actors
```
{
    "actors": [
        {
            "age": 38,
            "gender": "\"Female\"",
            "id": 7,
            "name": "\"Anne Hathaway\""
        }
    ],
    "success": true
}
```

#### DELETE /actors/{actor_id}
- General:
    - Deletes an actor based on actor ID if it exists.
    - Results contain the id of the actor deleted, the name, age, gender and success. 
```
{
    "actor": [
        {
            "age": 51,
            "gender": "Female",
            "id": 1,
            "name": "Cate Blanchett"
        },
    ],
    "success": true
}
```

## Authors
Andreea Monu 

## Acknowledgements 
The awesome team at Udacity teaching us new concepts and helping me become a full stack developer!