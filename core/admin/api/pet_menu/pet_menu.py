from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.models.pets_menu import PetMenu
from common.constants import user_constant


class MenuResource(Resource):
    def get(self):
        """
        get menu
        :return:
        """
        qs_parser = RequestParser()
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
        response_data['menuList'] = []
        filters = []

        order = PetMenu.id.asc() if _order == 1 else PetMenu.id.desc()
        try:
            paginate = PetMenu.query.filter(*filters).order_by(order).paginate(page_num, page_count, False)
        except Exception as e:
            current_app.logger.error(e)
            return response_to_api(code=1001)

        totalPages = paginate.pages
        currentPage = paginate.page
        items = paginate.items

        # get user info
        for menu_info in items:
            response_data['menuList'].append(menu_info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=0, data=response_data)

    def post(self):
        """
        create menu
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('name', required=False, location='json')
        json_parser.add_argument('menuId', required=False, location='json')
        json_parser.add_argument('icon', required=False, location='json')
        json_parser.add_argument('open', required=False, location='json')
        json_parser.add_argument('orderNum', required=False, location='json')
        json_parser.add_argument('parentId', required=False, location='json')
        json_parser.add_argument('parentName', required=False, location='json')
        json_parser.add_argument('perms', required=False, location='json')
        json_parser.add_argument('type', required=False, location='json')
        json_parser.add_argument('url', required=False, location='json')
        args = json_parser.parse_args()
        name = args.name
        menuId = args.menuId
        icon = args.icon
        open = args.open
        orderNum = args.orderNum
        parentId = args.parentId
        parentName = args.parentName
        perms = args.perms
        type = args.type
        url = args.url

        pet_menu = PetMenu()
        pet_menu.name = name
        pet_menu.menuId = menuId
        pet_menu.icon = icon
        pet_menu.open = open
        pet_menu.orderNum = orderNum
        pet_menu.parentId = parentId
        pet_menu.parentName = parentName
        pet_menu.perms = perms
        pet_menu.type = type
        pet_menu.url = url
        response_data = {}
        try:
            db.session.add(pet_menu)
            db.session.commit()
            response_data['MenuId'] = pet_menu.id
        except Exception as e:
            db.session.rollback()
        return response_to_api(code=0, data=response_data)
