from tinydb import TinyDB, Query
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
db = TinyDB('db.json')

@app.route('/')
def hello_world():
    data = {
        "app_name": "Special Blogger Monkey",
    }
    return render_template('index.html', data=data)
    return 'hey there!'

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = db.all()
    return jsonify(posts)

@app.route('/post', methods=['POST'])
def add_post():
    data = request.get_json()
    if not all([
        data.get('id'), data.get('title'),
    ]):
        return jsonify({"error": "Invalid post object"}), 400

    Post = Query()
    result = db.search(Post.id == int(data.get('id')))
    if result:
        return jsonify({"error": "A post with that id already exists"}), 400

    db.insert(data)
    return jsonify(data)

@app.route('/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    Post = Query()
    result = db.search(Post.id == int(post_id))
    if result:
        db.remove(Post.id == int(post_id))
        return jsonify({"message": "All ok"})
    return jsonify({"error": "No post with id {}".format(post_id)}), 404

@app.route('/post/<post_id>')
def get_specific_post(post_id):
    Post = Query()
    result = db.search(Post.id == int(post_id))
    if result:
        return jsonify(result)
    return jsonify({"error": "Post not found"}), 404
