import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_my_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}@{}/{}".format('ahmed:123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_categories(self):
        """
        get categories endpoint test_retrieve_categories function
        """
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])
        '''
        When Test it response is..

        Ran 1 test in 0.801s
       
        OK
        '''

    ''' test exist page of questions => page 1'''
    def test_paginate_questions(self):
        res = self.client().get('/questions?page=1')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
  
        '''
        When Test it response is..

        Ran 2 tests in 1.247s
      
        OK
        '''

    ''' test not exist page of questions => page 100'''
    def test_retrieve_all_questions_in_nonExistant_page(self):
        res = self.client().get('/questions?page=100')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')

        '''
        When Test it response is..

        AssertionError: 422 != 200

        Ran 3 tests in 2.388s 

        FAILED (failures=1)
        '''

    """
        get questions using test_retrieve_questions function
    """
    def test_retrieve_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

        '''
        When test runs it response successfulu

        Ran 3 tests in 1.796s

        OK
        '''
    """
        delete questions endpoint test function with valid id test_delete_question Func.
    """
    def test_delete_question(self):
        
        response = self.client().delete('questions/2')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        '''
        When test run it response successful

        Ran 4 tests in 2.268s

        OK
        '''
    """
        delete questions endpoint test_delete_question_422 function with Not valid id
    """
    def test_delete_question_422(self):
        response = self.client().delete('questions/5000')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertTrue(data['error'], 422)

        '''
        When test run it response Failed

        Ran 5 tests in 2.615s

        FAILED (failures=2)
        '''
    """
        test create question successfuly test_create_question
    """
    def test_create_question(self):
        
        new_question = {
            'question': 'Is it a test Ques cat2?',
            'answer': 'Yeah, It is',
            'category': '2',
            'difficulty': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')
        '''
        When test runs it response successful

        Ran 4 tests in 2.465s

        OK
        '''

    """
        get questions by category endpoint test_category_questions function
    """
    def test_category_questions(self):
        
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')

        '''
        When test runs it response successful

        Ran 5 tests in 2.424s

        OK
        '''
    
    """
        get questions by category error endpoint test_category_questions_422 function
    """
    def test_category_questions_422(self):
        
        response = self.client().get('/categories/15/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        '''FAILED (failures=1)'''

    """
        questions search endpoint test_search_for_question function
    """
    def test_search_for_question(self):
        
        response = self.client().post('/questions/search', json={'searchTerm': "what"})

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')
        '''Ran 6 tests in 2.771s OK'''


    """
        play quizz endpoint test_play_quizz function
    """
    def test_play_quizz(self):
        
        # response = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': '3'}})
        response = self.client().post("/quizzes", json={
            'quiz_category': {'type': 'Science', 'id': '1'},
            'previous_questions': []
        })
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()