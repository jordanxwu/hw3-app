from flask import Flask, jsonify, send_from_directory, request
import os
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
# from authlib.integrations.flask_client import OAuth


static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')
# Mongo connection
mongo_uri = os.getenv("MONGO_URI")
mongo = MongoClient(mongo_uri)
db = mongo["mydatabase"]


# oauth = OAuth(app)
# oauth.register(
#     name='dex',
#     server_metadata_url='http://localhost:5556/.well-known/openid-configuration',
#     client_id=os.getenv('OIDC_CLIENT_ID'),
#     client_secret=os.getenv('OIDC_CLIENT_SECRET'),
#     # client_kwargs={'scope': 'openid email profile groups'},
# )

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
CORS(app)

@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

@app.route("/test-mongo")
def test_mongo():
    return jsonify({"collections": db.list_collection_names()})

# ADDING COMMENTS
@app.route('/api/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    fields = ['article_id', 'user', 'text']
    for field in fields:
        if field not in data:
            return jsonify({'error': f'Missing field {field}'}), 400

    comment = {
        "article_id": data['article_id'],
        "user": data['user'],
        "text": data['text'],
        "parent_id": ObjectId(data['parent_id']) if data.get('parent_id') else None, # if replying to comment
        "removed": False
    }

    result = db.comments.insert_one(comment)
    return jsonify({'message': 'Comment added', 'id': str(result.inserted_id)}), 201

# GET COMMENTS
@app.route('/api/comments/<article_id>', methods=['GET'])
def get_comments(article_id):
    cursor = db.comments.find({"article_id": article_id})
    comments = []
    for comment in cursor:
        comments.append({
            "id": str(comment["_id"]),
            "article_id": comment["article_id"],
            "user": comment["user"],
            "text": comment["text"] if not comment.get("removed", False) else "COMMENT REMOVED BY MODERATOR!",
            "parent_id": str(comment["parent_id"]) if comment.get("parent_id") else None,
            "removed": comment.get("removed", False)
        })
    return jsonify(comments)


#DELETE COMMENTS
@app.route('/api/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    # Option A: actually delete the document
    result = db.comments.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Not found"}), 404
    return '', 204

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)),debug=debug_mode)