from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import Comments
from app import db
from flask_jwt_extended import jwt_required,get_jwt_identity


comment = Blueprint('comment', __name__)

@comment.route('/post/<int:pid>/add', methods = ['GET', 'POST'], endpoint='add_comment')
@jwt_required()
def add_comment(pid):

        if request.method == 'POST':

            content = request.form.get('content')

            if not content:
                 return jsonify({"message":"Content is missing","status":"error"}), 401
            
            current_user_id = get_jwt_identity()

            add_comment = Comments(
                    post_id = pid,
                    user_id = current_user_id,
                    content = content,
                    created_at = datetime.now() 
            )

            db.session.add(add_comment)
            db.session.commit()
            return jsonify({"message": "Comment is added successfully", "status": "success"}), 200

                
        if request.method == 'GET':
            return jsonify({"message":"Add Comment","status":"pending"}), 202


@comment.route('/post/<int:pid>/edit/<int:cid>', methods = ['GET', 'PUT','PATCH'] ,endpoint = 'edit_comment')
@jwt_required()
def edit_comment(pid,cid):

    if request.method in ['PUT', 'PATCH']:
       
            content = request.form.get('content')

            if not content:
                 return jsonify({"message":"Content is missing","status":"error"}), 401
            
            current_user_id = get_jwt_identity()

            comment = Comments.query.filter_by(comment_id=cid, post_id=pid, user_id=current_user_id).first()
        
            if not comment:
                return jsonify({"message": "Comment not found ", "status": "error"}), 402
        
            comment.content = content
            comment.updated_at = datetime.now()
            db.session.commit()
            return jsonify({"message": "Comment is edited successfully", "status": "success"}), 200
            
    if request.method == 'GET':
        return jsonify({"message":"Edit Comment","status":"pending"}), 202





@comment.route('/post/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    comments = Comments.query.filter_by(post_id=post_id).all()
    return jsonify([{'cid': comment.comment_id, 'content': comment.content} for comment in comments])
