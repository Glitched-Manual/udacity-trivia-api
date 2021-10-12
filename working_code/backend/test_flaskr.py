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
        self.database_name = "trivia_test"
        #self.password = ""
        self.database_path = "postgresql://student:student@{}/{}".format('localhost:5432', self.database_name)
        #self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
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
    
    Write at least one test for each test for successful operation and for expected errors.
    """

    """
    / category test
    """

    def test_get_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['categories'], True)

    def test_404_request_category_not_found(self):
        res = self.client().get('/categories/9000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """
    /questions tests
    
    """
        
    def test_get_paginated_questions(self):
        """Test to get some question from the database"""

        res = self.client().get('/questions')
        data = json.loads(res.data)

        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

        self.assertTrue(len(data['categories']))

    """
    Test for page of questions that does not exist
    """
    def test_404_page_not_found_request(self):

        res = self.client().get('/questions?page=9000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    """
    /question delete tests

    """
    
    def test_delete_question(self):

        #create question to delete for test
        test_question = Question(question='question', answer='answer', category=1, difficulty=1)
        test_question.insert()
        
        test_question_id = test_question.id

        # call delete method

        res = self.client().delete(f'/questions/{test_question_id}')
        data = json.loads(res.data)

        # check for success code and message
        self.assertTrue(res.status_code, 200)
        self.assertTrue(data['success'], True)

        #check if te correct question was deleted
        self.assertEqual(str(data['deleted']), str(test_question_id))

        #check if the created question is now None or Null value
        self.assertTrue(test_question, None)


    def test_422_for_deleting_question_that_does_not_exist(self):

        res = self.client().delete('/questions/1000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_create_question(self):
       
        before_create_questions_length = len(Question.query.all())

        test_question = {'question':'question', 'answer':'answer', 'category':2, 'difficulty':2}
       

        res = self.client().post('/questions', json=test_question)
        data = json.loads(res.data)

        after__create_questions_length = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(before_create_questions_length, after__create_questions_length - 1)


    def test_422_create_question_error(self):

        before_create_questions_length = len(Question.query.all())

        # create question method wit blank dict

        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        # questions after post request

        after__create_questions_length = len(Question.query.all())

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
        #check if question before and after lengths are the same
        self.assertEqual(before_create_questions_length, after__create_questions_length)


    def test_search_questions(self):

        res = self.client().post('questions/search', json={'searchTerm': 'm'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['totalQuestions'])

    def test_404_search_questions_error(self):
        # search blank
        res = self.client().post('questions/search', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    """
    /categories/<int:category_id>/questions
    
    """
    
    def test_get_category_questions(self):
        #get questions from an existing
        res = self.client().get('/categories/2/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        """
        'questions': [question.format() for question in questions],
        'total_questions': len(questions)
            
        """
        self.assertTrue(len(data['questions']), True)
        self.assertTrue(data['total_questions'], True)

    def test_404_none_existing_category(self):

        res = self.client().get('/categories/9000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_play_quiz(self):
        test_quiz_round = {'previous_questions': [],
                            'quiz_category': { 'type': 'Art', 'id': 2}}

        res = self.client().post('/quizzes', json=test_quiz_round)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        self.assertTrue(data['question']['category'], 2)
        """
        category = body.get('quiz_category')
        previous_questions =  body.get('previous_questions')
        2 | Art

        new_quiz_round = {'previous_questions': [],
                          'quiz_category': {'type': 'Entertainment', 'id': 5}}
        """
    def test_404_quiz_error(self):
        #test_quiz_round = {'previous_questions', []}
        res = self.client().post('/quizzes', json={})

        data = json.loads(res.data)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()