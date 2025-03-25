# Scores API

A Flask API for storing and retrieving user scores for the Augmented Reality Geoguessr project.

## Project Overview

The Scores API is a crucial component of the Augmented Reality Geoguessr application, designed to handle all score-related operations. This API provides endpoints for storing, retrieving, updating, and deleting user scores, enabling the application to maintain leaderboards and track player progress.

## Features

- Store user scores with associated metadata
- Retrieve scores for specific users
- Get top scores across all users
- Update and delete existing scores
- Simple and intuitive RESTful API design
- Firebase Realtime Database integration for persistent storage

## Prerequisites

Before setting up the Scores API, ensure you have the following:

- Python 3.8 or higher
- pip (Python package manager)
- Firebase project with Realtime Database enabled
- Firebase Admin SDK credentials file

## Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/Augmented-Reality-Geoguessr/ScoresAPI.git
   cd ScoresAPI
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following content:
   ```
   # Firebase Configuration
   FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
   FIREBASE_CREDENTIALS_FILE=path-to-your-credentials-file.json

   # Flask Configuration
   FLASK_APP=scores.py
   FLASK_ENV=development
   PORT=5000
   ```

4. Place your Firebase credentials file in the root directory.

## Firebase Setup

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Navigate to Project Settings > Service Accounts
4. Generate a new private key for the Firebase Admin SDK
5. Save the JSON file to your project directory
6. Enable the Realtime Database in your Firebase project

## Running the Application

Start the API server:
```
python scores.py
```

The API will be available at `http://localhost:5000/`.

## API Endpoints

### Get All Scores
- **URL**: `/scores`
- **Method**: `GET`
- **Description**: Retrieves all scores from the database
- **Response**: JSON object containing all score records

### Get Scores for a Specific User
- **URL**: `/scores?user_id=`
- **Method**: `GET`
- **Description**: Retrieves all scores for a specific user
- **Response**: JSON object containing the user's score records

### Get Top Scores
- **URL**: `/scores/top?count=`
- **Method**: `GET`
- **Description**: Retrieves the top scores across all users
- **Parameters**: `count` (optional) - Number of top scores to retrieve (default: 10)
- **Response**: JSON array of score objects sorted by score in descending order

### Get User Scores (Alternative Endpoint)
- **URL**: `/users//scores`
- **Method**: `GET`
- **Description**: Retrieves all scores for a specific user
- **Response**: JSON object containing the user's score records

### Add a New Score
- **URL**: `/scores`
- **Method**: `POST`
- **Description**: Adds a new score record to the database
- **Request Body**:
  ```json
  {
    "user_id": "123",
    "username": "player1",
    "score": 500,
    "game_details": {
      "level": "hard",
      "time_spent": 120
    }
  }
  ```
- **Response**: JSON object containing the new score's ID and data

### Update a Score
- **URL**: `/scores/`
- **Method**: `PUT`
- **Description**: Updates an existing score record
- **Request Body**:
  ```json
  {
    "score": 750,
    "username": "updated_name",
    "game_details": {
      "level": "expert"
    }
  }
  ```
- **Response**: JSON object confirming the update

### Delete a Score
- **URL**: `/scores/`
- **Method**: `DELETE`
- **Description**: Deletes a score record from the database
- **Response**: JSON object confirming the deletion

## Dependencies

- Flask: Web framework for building the API
- Firebase Admin SDK: Interface for Firebase Realtime Database
- python-dotenv: Loading environment variables from .env file
- gunicorn: WSGI HTTP server for deployment (optional)

## Issues

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.