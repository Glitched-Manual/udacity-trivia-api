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

Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) using the project directory. Then install the backend requirements by navigating to `/backend` in the terminal and run:

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
flask run
```

### On MAC / Linux bash

```bash
export FLASK_APP=flaskr
flask run
```

## Starting the frontend in Developer mode

-----
To run the app in development mode. Navigate to the `frontend` directory and run:

```bash
npm start
```

