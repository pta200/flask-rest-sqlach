from flask import request
from flask_restful import Resource
from models import db, ma, Post, PostSchema, uuid
from credentials import jwt_required

class PostListResource(Resource):
    # list all posts
    @jwt_required()
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)
    # create new post
    @jwt_required()
    def post(self):
        new_post = Post(
            post_id=uuid.uuid4(),
            title=request.json['title'],
            content=request.json['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

class PostResource(Resource):
    # get post by id
    @jwt_required()
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)
    
    # update post
    @jwt_required()
    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)

    # delete post
    @jwt_required()
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

# instantiate json post schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)