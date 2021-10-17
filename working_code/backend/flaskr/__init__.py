import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from random import randint
import random
import sys

from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

  '''
 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      categories = Category.query.order_by(Category.type).all()

      category_dictionary = {}

      for category in categories:
        category_dictionary[category.id] = category.type

      if len(categories) < 1:
        abort(404)

      #formated_categories = [category.format() for category in categories]

      return jsonify({
        'success': True,
        'categories': category_dictionary
    })

  '''
  
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
  def get_questions():
       all_questions = Question.query.order_by(Question.id).all()
       total_questions = len(all_questions)
       selected_questions = paginate_questions(request, all_questions)

       if len(selected_questions) == 0:
        abort(404)
       
       categories = Category.query.order_by(Category.type).all()

       category_dictionary = {}

       for category in categories:
        category_dictionary[category.id] = category.type

       if len(categories) < 1:
         abort(404)

       return jsonify({
          'success': True,
          'questions': selected_questions,
          'categories': category_dictionary,
          'total_questions': total_questions,
           })

  '''  

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      else:
        question.delete()

        return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                   
                }
        )
      
    except:
      abort(422)


  '''
  
  Create an endpoint to POST a new question, 
  which will *require* the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=["POST"])
  def create_question():
    
    body = request.get_json()      
    question = body.get('question')
    answer = body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')
    
    # make sure no null valus are found
    question_parts = [question,answer,difficulty,category]

    for part in question_parts:
      
      if part is None:
        abort(422)
    try:  
        db_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
        db_question.insert()

        return jsonify({
            'success': True,
            'created': db_question.id
            })

    except:
          
      abort(422)
     
  '''
 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=["POST"])
  def search_questions():
    try:
      body = request.get_json()
      
      search_query = body.get('searchTerm', None)

      if search_query == '':
        abort(404)

      if search_query:
        search_results = Question.query.filter(Question.question.ilike(f'%{search_query}%'))
        questions_found = [question.format() for question in search_results]
      
        if len(questions_found) == 0:
          abort(404)        

        return jsonify({
          'success': True,
          'questions': questions_found,
          'totalQuestions': len(questions_found),
          'currentCategory': None
        })
    except:
      abort(404)

    
  '''
  
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=["GET"])
  def get_questions_by_category(category_id):
    try:              
     
      questions = Question.query.filter(Question.category == str(category_id)).all()
      
      if len(questions) < 1 :
          abort(404)

      return jsonify({        
          'success': True,
          'questions': [question.format() for question in questions],
          'total_questions': len(questions),
          'current_category': category_id        
      })

      
    except:
      abort(404)



  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=["POST"])
  def play_quiz():
    try:
       

        body = request.get_json()
        
        if (body.get('quiz_category') == None) or (body.get('previous_questions') == None):
          
            abort(422)

        category = body.get('quiz_category')
        previous_questions =  body.get('previous_questions')

        quiz_question = null

        if category['type'] == 'click':
            available_questions = Question.query.filter((Question.id.notin_(previous_questions))).all()

        else:
          
            available_questions = Question.query.filter(Question.category == str(category['id'])).filter((Question.id.notin_(previous_questions))).all()
        
        total_available_questions = len(available_questions)

        if total_available_questions > 0:
            quiz_question = available_questions[randint(0,total_available_questions)].format()
        
        # return the question
        return jsonify({
            'success': True,
            'question': quiz_question
        })
    except:

      print("******************************")
      print(sys.exc_info())
      print("******************************")

      abort(422)
  
  @app.errorhandler(400)
  def bad_request(error):
        return (
          jsonify({"success": False, "error": 400, "message": "bad request"}), 
        400,
        ) 
  
  @app.errorhandler(404)
  def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

  @app.errorhandler(422)
  def unprocessable(error):
          return (
              jsonify({"success": False, "error": 422, "message": "unprocessable"}),
              422,
          )
  

  return app

    