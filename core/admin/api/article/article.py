from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models.pets_article import PetsArticle
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.constants import user_constant


class Article(Resource):
    """文章列表"""

    def get(self):
        """
        获取文章列表
        :return:
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('name', required=False, location='args')
        qs_parser.add_argument('title', required=False, location='args')
        qs_parser.add_argument('user_id', required=False, location='args')
        qs_parser.add_argument('order', type=inputs.positive, required=False, location='args')
        qs_parser.add_argument('pageNum', type=inputs.positive, required=False, location='args')
        qs_parser.add_argument('pageSize', required=False,
                               type=inputs.int_range(user_constant.DEFAULT_USER_PER_PAGE_MIN,
                                                     user_constant.DEFAULT_USER_PER_PAGE_MAX,
                                                     'pageSize'))

        args = qs_parser.parse_args()
        _order = args.order
        page_num = 1 if args.pageNum is None else args.pageNum
        page_count = args.pageSize if args.pageSize else user_constant.DEFAULT_USER_PER_PAGE_MIN
        response_data = {}
        response_data['details'] = []
        filters = []

        if args.title is not None:
            filters.append(PetsArticle.title.like('%' + args.title + '%'))

        order = PetsArticle.id.asc() if _order == 1 else PetsArticle.id.desc()
        try:
            paginate = PetsArticle.query.filter(*filters).order_by(order).paginate(page_num)
        except Exception as e:
            print('some error happen %s', e)

        totalPages = paginate.pages
        currentPage = paginate.pages
        items = paginate.items

        for info in items:
            response_data['details'].append(info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=200, data=response_data)

    def post(self):
        """
        创建文章
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('user_id', required=True, location='json')
        json_parser.add_argument('pet_id', required=True, location='json')
        json_parser.add_argument('title', required=False, location='json')
        json_parser.add_argument('content', required=False, location='json')
        args = json_parser.parse_args()
        user_id = args.user_id
        pet_id = args.pet_id
        title = args.title
        content = args.content

        article = PetsArticle()
        article.user_id = user_id
        article.pet_id = pet_id
        article.title = title
        article.content = content
        response_data = {}
        try:
            db.session.add(article)
            db.session.commit()
            response_data['ArticleId'] = article.id
        except Exception as e:
            db.session.rollback()
        return response_to_api(code=200, data=response_data)

