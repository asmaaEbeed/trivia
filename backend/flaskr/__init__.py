import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, OPTIONS, DELETE, PATCH')
        return response
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        '''
        Handles GET requests for getting all categories.
        '''
        try:
            # get all categories and add to dict
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.cat_type

            # abort 404 if no categories found
            if (len(categories_dict) == 0):
                abort(404)
            else:
                # return data to view
                return jsonify({
                    'success': True,
                    'categories': categories_dict,
                    'status_code': 200,
                    'total_categories': len(categories),
                    'status_message': 'OK'
                })
        except Exception:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def retrieve_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)
            categories = Category.query.order_by(Category.id).all()
            cat_items = [(
                category.id, category.cat_type) for category in categories]

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": list(set([question['category'] for question in current_questions])),
                "categories": {key: value for (key, value) in cat_items}
            })

        except Exception:
            abort(422)
    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success':  True,
                'deleted': question_id,
                'question': current_questions,
                'total_questions': len(selection),
                'status_message': 'OK'
            })
        except:
            abort(422)
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        # Check if field is empty
        if question == '' or answer == '' or category == '' or difficulty == '':
            abort(422)

        try:
            question = Question(question=question, answer=answer, difficulty=difficulty, cat_Id=category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success':  True,
                'question': current_questions,
                'total_questions': len(selection),
                'status_message': 'OK'
            })
        except:
            abort(422)
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_for_question():
        search_term = request.get_json()['searchTerm']
        try:
            selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
            current_question = paginate_questions(request, selection)
            return jsonify({
                    'success': True,
                    'questions': current_question,
                    'currentCategory': list(set([question['category'] for question in current_question])),
                    'totalQuestions': len(selection),
                    'status_message': 'OK'
                })
        except:
            abort(500)
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def category_questions(cat_id):
        try:
            questions = Question.query.filter(Question.cat_Id == cat_id).all()
            current_questions = paginate_questions(request, questions)
            current_category = Category.query.get(cat_id)
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(questions),
                'currentCategory': current_category.format(),
                'status_message': 'OK'
            })
        except:
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        category = body.get('quiz_category').get('id')
        previous_questions = body.get('previous_questions')
        if(category == 0):
            all_questions = Question.query.all()
        else:
            all_questions = Question.query.filter(Question.cat_Id == category).all()

        if len(all_questions) == 0:
            abort(404)

        if len(all_questions) == len(previous_questions):
            return jsonify({
                'success': True,
                'question': None,
            })
        else:
            random_questions = []

            #append all available question that not asked before in tandom_questions list
            for question in all_questions:
                if question.id not in previous_questions:
                    random_questions.append(question.format())
           # Choose random question from random_questions list
            selected_question = random_questions[random.randint(0, len(random_questions)-1)]
            return jsonify({
                'success': True,
                'question': selected_question,
                'status_message': 'OK'
            })
        
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "not found"
        }), 405
    return app

    