from flask import Flask
from models import db, ma, Post, PostSchema, RevokedTokenModel
import apis, credentials
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# app factory
def create_app(test_config=None):
    # init app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init sqlalchemy and marshmallow
    db.app = app
    db.init_app(app)
    ma.init_app(app)

    # init jwt
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # regiser jtw
    jwt = JWTManager(app)

    # check it token is on blacklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(header,decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

    # init flask restful
    api = Api(app)
    CORS(app)

    # register apis
    api.add_resource(apis.PostListResource, '/posts')
    api.add_resource(apis.PostResource, '/posts/<int:post_id>')
    api.add_resource(credentials.UserRegistration, '/registration')
    api.add_resource(credentials.UserLogin, '/login')
    api.add_resource(credentials.UserLogoutAccess, '/logout/access')
    api.add_resource(credentials.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(credentials.TokenRefresh, '/token/refresh')
    api.add_resource(credentials.AllUsers, '/users')
    #api.add_resource(credentials.SecretResource, '/secret')
    return app

if __name__=='__main__':
    app = create_app()
    app.run(debug=True)
