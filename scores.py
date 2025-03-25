from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os
import config

app = Flask(__name__)

# Initialize Firebase with your credentials
cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_FILE)
firebase_admin.initialize_app(cred, {
    'databaseURL': config.FIREBASE_DATABASE_URL
})

# Reference to the scores in the database
scores_ref = db.reference('scores')

@app.route('/scores', methods=['GET'])
def get_scores():
    """Get all scores or filter by user_id"""
    user_id = request.args.get('user_id')
    
    if user_id:
        # Get scores for a specific user
        user_scores = scores_ref.order_by_child('user_id').equal_to(user_id).get()
        return jsonify(user_scores)
    else:
        # Get all scores
        all_scores = scores_ref.get()
        return jsonify(all_scores or {})

@app.route('/scores/top', methods=['GET'])
def get_top_scores():
    """Get top scores, optionally limited by count"""
    count = request.args.get('count', 10, type=int)
    
    # Get scores ordered by score value (descending)
    top_scores = scores_ref.order_by_child('score').limit_to_last(count).get()
    
    if not top_scores:
        return jsonify([])
        
    # Convert to list and reverse to get descending order
    scores_list = [{"id": k, **v} for k, v in top_scores.items()]
    scores_list.sort(key=lambda x: x['score'], reverse=True)
    
    return jsonify(scores_list)

@app.route('/scores', methods=['POST'])
def add_score():
    """Add a new score entry"""
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ('user_id', 'username', 'score')):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create score entry
    score_entry = {
        'user_id': data['user_id'],
        'username': data['username'],
        'score': data['score'],
        'timestamp': datetime.now().isoformat(),
        'game_details': data.get('game_details', {})
    }
    
    # Generate a unique ID and push to Firebase
    new_score_ref = scores_ref.push(score_entry)
    
    return jsonify({
        "id": new_score_ref.key,
        "message": "Score added successfully",
        "data": score_entry
    }), 201

@app.route('/scores/<score_id>', methods=['PUT'])
def update_score(score_id):
    """Update an existing score"""
    data = request.get_json()
    
    # Check if score exists
    score = scores_ref.child(score_id).get()
    if not score:
        return jsonify({"error": "Score not found"}), 404
    
    # Updated fields
    updated_data = {}
    for key in ['score', 'username', 'game_details']:
        if key in data:
            updated_data[key] = data[key]
    
    scores_ref.child(score_id).update(updated_data)
    
    return jsonify({
        "message": "Score updated successfully",
        "id": score_id
    })

@app.route('/scores/<score_id>', methods=['DELETE'])
def delete_score(score_id):
    """Delete a score"""
    # Check if score exists
    score = scores_ref.child(score_id).get()
    if not score:
        return jsonify({"error": "Score not found"}), 404
    
    # Delete the score
    scores_ref.child(score_id).delete()
    
    return jsonify({
        "message": "Score deleted successfully",
        "id": score_id
    })

@app.route('/users/<user_id>/scores', methods=['GET'])
def get_user_scores(user_id):
    """Get all scores for a specific user"""
    user_scores = scores_ref.order_by_child('user_id').equal_to(user_id).get()
    return jsonify(user_scores or {})

# Add a simple health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "API is running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /scores": "Get all scores",
            "GET /scores?user_id=<user_id>": "Get scores for specific user",
            "GET /scores/top?count=<count>": "Get top scores",
            "GET /users/<user_id>/scores": "Get all scores for specific user",
            "POST /scores": "Add a new score",
            "PUT /scores/<score_id>": "Update a score",
            "DELETE /scores/<score_id>": "Delete a score"
        }
    })

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=True)
