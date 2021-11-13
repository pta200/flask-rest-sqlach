from flask import Flask
from models import db, ma, Post, PostSchema
from apis import PostResource, PostListResource
from flask_restful import Api

# init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init sqlalchemy and marshmallow
db.app = app
db.init_app(app)
ma.init_app(app)

# init flask restful
api = Api(app)

# register apis
api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')

if __name__=='__main__':
    app.run(debug=True)
