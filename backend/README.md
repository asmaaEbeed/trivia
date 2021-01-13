# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

```GET '/categories'```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
    - `status_code`: contains the response status code.
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `total_categories`: the number of questions returned. 

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
  "status_code": 200, 
  "success": true, 
  "total_categories": 6
}

```
```GET '/questions'```
- Fetches a dictionary of question.
- Request Arguments: by page number like that ```/questions?page=1``` or only ```/questions``` to get all question.
- Returns: An object with that structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: return `OK` if it's success.
    - `questions`: return list with each questions info.
    - `total_questions`: return total number of questions.
    - `current_category`: retuen list of question category in current page.
    - `categories`: return object with all category.

- Samples of return:
```{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    3, 
    4, 
    5, 
    6
  ], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 1, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
    ... similar 10 question in one page
  ], 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_questions": 19
}
```
```DELETE '/questions/<int:question_id>'```
- Deletes the question selectecd by `question_id`.
- Returns: An object with that structure:
    - `success`:  take values `True` when successfullnes of the endpoint's execution.
    - `deleted`: question ID that deleted.
    - `question`: return list with each questions info.
    - `total_questions`: return total number of questions.

```POST '/questions'```
- To post new question, will require the question and answer text, category, and difficulty score from ```request.get_json()```
- Sure All of then not empty
- Insert new question in database
- Then empty it's value
- Returns: An object with that structure:
    - `success`: can take values `True` deppending on the successfullnes of the endpoint's execution.
    - `question`: return list with each questions info.
    - `total_questions`: return total number of questions after add new one.

```POST '/questions/search'```
- Return questions based on a search term.
- Request Arguments:
  - ```searchTerm``` string of question or part of question that I search with regardless case sensetive.
- Returns: object with the following structure:
  - `success`: can take values `True` deppending on the successfullnes of the endpoint's execution.
  - `questions`: retuen list of question category in current page.,
  - `current_category`: retuen list of question category in current page.
  - `totalQuestions`: return total number of questions after add new one.


```POST '/quizzes'```
- start game
- Request Arguments:
  - ```category_id```: id of category selected and if selected all id will equal 0.
  - ```previous_quesion```: all previous question asked in game, first time it's an empty string.
- Returns: object with the following content:
  - `success`: can take values `True` deppending on the successfullnes of the endpoint's execution.
  - `question`: contains the question. Question is object containing id, question, answer, category and diffficulty.

## CURL Commands test

 - To delete items testing using CURL 
    ```curl -X DELETE http://127.0.0.1:5000/questions/2  ```   
 - To get questions
    ```curl -X GET http://127.0.0.1:5000/questions```

- To POST new question



- GET question according to specific category
  ```http://127.0.0.1:5000/categories/2/questions```
  
  ```````

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

- get categories endpoint test function
  ```/categories```
  Run success
  '''
        When Test it response is..

        Ran 1 test in 0.801s
       
        OK
    '''
  
  - test exist page of questions => page 1 using test_paginate_questions function
    ```'/questions?page=1'```
    Run sucess
    '''
        When Test it response is..

        Ran 2 tests in 1.247s
      
        OK
    '''

  - test not exist page of questions => page 100
    ```/questions?page=100```
    FAILED
    '''
         When Test it response is..

         AssertionError: 422 != 200

         Ran 3 tests in 2.388s 

         FAILED (failures=1)
    '''
  
  - test get questions using test_retrieve_questions function
    ```/questions```
    RUN success
    '''
    When test runs it response successfulu

    Ran 3 tests in 1.796s

    OK
    '''

  - delete questions endpoint test function with valid id test_delete_question Func.
    ```questions/2```
    RUN success
    '''
    Ran 4 tests in 2.268s

    OK
    '''

  - delete questions endpoint test_delete_question_422 function with Not valid id
    ```questions/2```
    FAILED
    '''
    Ran 5 tests in 2.615s

    FAILED (failures=2)
    '''

  - test create question successfuly test_create_question
    ```/questions```
    RUN success
    '''
    Ran 4 tests in 2.465s

    OK
    '''

  - get questions by category endpoint test_category_questions function
    ```/categories/1/questions```
    RUN success
    '''
    Ran 5 tests in 2.424s

    OK
    '''

  - get questions by category error endpoint test_category_questions_422 function
    ```/categories/15/questions```
    FAILED
    '''
    FAILED
    (failures=1)

    '''

  - questions search endpoint test_search_for_question function
    ```/questions/search```
    RUN success
    '''
    Ran 6 tests in 2.771s 
    OK
    '''

  - play quizz endpoint test_play_quizz function
    ```/quizzes```
      post with quiz_category, previous_questions
      RUN SUCCESS
      '''
      Ran 7 tests in 3.298s
      OK
      '''