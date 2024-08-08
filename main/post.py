from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from werkzeug.utils import secure_filename
from .models import Posts
from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from .drive import upload_image_to_drive, get_image_url

post = Blueprint('post', __name__)



@post.route('/create_post', methods=['GET','POST'])
@jwt_required()
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_file = request.files.get('image')

        if not title:
            return jsonify({"message": "Title is missing", "status": "error"}), 400

        if not content:
            return jsonify({"message": "Content is missing", "status": "error"}), 400

        current_user_id = get_jwt_identity()

        image_url = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            file_id = upload_image_to_drive(image_file, filename)
            image_url = get_image_url(file_id)
           

        new_post = Posts(
            title=title,
            content=content,
            image=image_url,
            mimetype=image_file.mimetype if image_file else None,
            created_at=datetime.now(),
            author_id=current_user_id
        )

        try:
            db.session.add(new_post)
            db.session.commit()
            return jsonify({"message": "New post is added successfully", "status": "success"}), 201
            
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Failed to add post", "status": "error"}), 500

    if request.method == 'GET':
            return jsonify({"message":"Add Post","status":"pending"}), 202



@post.route('/edit_post/<int:id>', methods=['GET','POST'])
@jwt_required()
def edit_post(id):
    if request.method == 'POST':
        current_user_id = get_jwt_identity()
        editpost = Posts.query.filter_by(post_id=id).first()

        if not editpost:
            return jsonify({"message": "Post not found", "status": "error"}), 404

        if editpost.author_id != current_user_id:
            return jsonify({"message": "Unauthorized", "status": "error"}), 403

        title = request.form.get('title')
        content = request.form.get('content')
        image_file = request.files.get('image')

        if title:
            editpost.title = title
        if content:
            editpost.content = content

        if image_file and image_file.filename != '':
           
            editpost.image = get_image_url(file_id)
            editpost.mimetype = image_file.mimetype

        editpost.updated_at = datetime.now()

        db.session.commit()
        return jsonify({"message": "Post is updated successfully", "status": "success"}), 200

    if request.method == 'GET':
            return jsonify({"message":"Edit Post","status":"pending"}), 202


@post.route('/delete_post/<int:pid>', methods=['GET','POST'])
@jwt_required()
def delete_post(pid):
    if request.method == 'POST':
        current_user_id = get_jwt_identity()
        deletepost = Posts.query.filter_by(post_id=pid).first()

        if not deletepost:
            return jsonify({"message": "Post not found", "status": "error"}), 404

        if deletepost.author_id != current_user_id:
            return jsonify({"message": "Unauthorized", "status": "error"}), 403

        db.session.delete(deletepost)
        db.session.commit()
        return jsonify({"message": "Post is deleted successfully", "status": "success"}), 200
    
    if request.method == 'GET':
            return jsonify({"message":"Delete the post","status":"pending"}), 202


@post.route('/viewpost', methods=['GET'])
@jwt_required()
def all_post():
    posts = Posts.query.all()
    posts_list = []


    for post in posts:
        user = Users.query.get(post.author_id)
        post_data = {
            'post_id': post.post_id,
            'author_id': post.author_id,
            'author_username': user.username,
            'title': post.title,
            'content': post.content,
            'image_url': post.image,
            'mimetype': post.mimetype,
            'created_at': post.created_at,
            'updated_at': post.updated_at
        }
        posts_list.append(post_data)

    return jsonify({"posts": posts_list}), 200
