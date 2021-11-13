from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
import sqlalchemy_utils

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

