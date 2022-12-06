from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models.recipe import Recipe
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.constants import user_constant


class RecipeResource(Resource):
    """

    """

    def get(self):
        qs_parser = RequestParser()
        qs_parser.add_argument('name', required=False, location='args')
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

        if args.name is not None:
            filters.append(Recipe.name.like('%' + args.name + '%'))

        order = Recipe.id.asc() if _order == 1 else Recipe.id.desc()
        try:
            paginate = Recipe.query.filter(*filters).order_by(order).paginate(page_num)
        except Exception as e:
            print('some error happen %s', e)

        totalPages = paginate.pages
        currentPage = paginate.pages
        items = paginate.items

        for recipe_info in items:
            response_data['details'].append(recipe_info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=200, data=response_data)

    def post(self):
        """
        创建食谱
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('weight', required=False, location='json')
        json_parser.add_argument('cook_time', required=False, location='json')
        json_parser.add_argument('remark', required=False, location='json')
        args = json_parser.parse_args()
        name = args.name
        weight = args.weight
        cook_time = args.cook_time
        remark = args.remark

        recipe = Recipe()
        recipe.name = name
        recipe.weight = weight
        recipe.cook_time = cook_time
        recipe.remark = remark
        response_data = {}
        try:
            db.session.add(recipe)
            db.session.commit()
            response_data['RecipeId'] = recipe.id
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
        return response_to_api(code=200, data=response_data)



