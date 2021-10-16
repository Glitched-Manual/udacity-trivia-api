# Full Stack Trivia API Project

This trivia API project is a completed version of the Udacity Full Stack trivia exerience. This project utilzes python Flask for the backend and Node.js for the frontend for the application.

The application contains the following features:


1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting started

-----

### Needed Skills

Developers who wish to use this project must have the following tools installed:

- [Python3](https://www.python.org/downloads/)
- pip (Typicaly included with Python3 install)
- [Node](https://nodejs.org/en/download/)
- npm (included with Node )

## Project Dependancies

-----
To get started clone or copy the and extract the zip file of this project to the desired project directory

### Backend Dependancies

Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) using the project directory or the `/backend` directory. Then install the backend requirements by navigating to `/backend` in the terminal and run:

```bash
pip install -r requirements.txt
```

### Frontend Dependancies

The frontend dependancies are aquired via using NPM. To get the needed packages NPM needs the `package.json` file that is located in the `/frontend` directory. To install the packages navigate to the `/frontend` directory in your terminal, then run:

```bash
npm install
```

## Starting the Server
-----
In the `/backend` directory that is within your virtual environment.

run the server by excuting:

### On Windows CMD

```cmd
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

### On MAC / Linux bash

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Starting the frontend in Developer mode

-----
To run the app in development mode. Navigate to the `/frontend` directory and run:

```bash
npm start
```

Open http://localhost:3000 to view the frontend site in your browser. The page will reload if you make edits.

## Tests
-----
To run Test navigate to `/backend` and run the script `test_flaskr.py`

```bash
python3 test_flaskr.py
```


## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`.

- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling

Errors are returned in the form of JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints

#### Get /categories

- General:

  - returns all available categories

- Sample: `curl http://localhost:5000/categories`

```bash
{
  "categories": {
    "1": "Science",       
    "2": "Art",
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  },
  "success": true
}
```

#### Get /questions

- General:
  - returns the available categories
  - Returns a list of question objects, success value, and total number of questions
  - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.

- Sample: `curl http://127.0.0.1:5000/questions`

```bash
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
  "total_questions": 20
}
```

#### Delete /questions/<int:question_id>

- General:
  - deletes the question that matches the given id passed to the end point
  - returns a success message if the target object was successfully deleted

- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/9`

```bash
{
  "deleted": 9,
  "success": true
}
```

#### Post /questions

- General:
  
  - creates a new question
  - returns success when the new question is added

- Sample (windows): `curl -H "Content-Type: application/json" -X POST -d {\"question\":\"question\",\"answer\":\"easy\",\"difficulty\":\"1\",\"category\":\"1\"} http://localhost:5000/questions`

- Sample (Linux): `curl -H "Content-Type: application/json" -X POST -d '{"question":"new question", "answer":"easy answer", "difficulty":"1", "category":"1"}' http://localhost:5000/questions`

```bash
{
  "created": 25,
  "success": true
}```

