from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# sql blog post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title

# marshmallow json post model for api responses
class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")
        model = Post

