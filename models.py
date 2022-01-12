"""
SQLAlchemy models file.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
import sqlalchemy_utils
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()
ma = Marshmallow()

# sql blog post model
class Post(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(sqlalchemy_utils.UUIDType(binary=True), primary_key=True, nullable=False)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title

# marshmallow json post model for api responses
class PostSchema(ma.Schema):
    class Meta:
        fields = ("post_id", "title", "content")
        model = Post

#jwt user class
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username
                #,'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

# revoked token
class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)