from flask import Blueprint
from flask_restful import Api
from core.admin.api.article import article

article_bp = Blueprint('article', __name__)
article_api = Api(article_bp)

article_api.add_resource(article.Article, '/api/article/list', endpoint='ArticleListResource')
article_api.add_resource(article.Article, '/api/article/create', endpoint='ArticleCreateResource')
