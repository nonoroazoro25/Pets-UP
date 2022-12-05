from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.constants import user_constant
from common.models.pets import Pet
from common.utils.response_util import response_to_api
from common.models import db


class PetsResource(Resource):
    """
    宠物
    """

    def get(self):
        """
        宠物列表
        :return:
        """
        print('pets list')
        qs_parser = RequestParser()
        qs_parser.add_argument('name', required=False, location='args')
        qs_parser.add_argument('type', required=False, location='args')
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
        response_data['users'] = []
        filters = []

        if args.name is not None:
            filters.append(Pet.name.like('%' + args.email + '%'))
        if args.type is not None:
            filters.append(Pet.type.like('%' + args.email + '%'))

        order = Pet.id.asc() if _order == 1 else Pet.id.desc()
        try:
            paginate = Pet.query.filter(*filters).order_by(order).paginate(page_num)
        except Exception as e:
            print('some error happen %s', e)

        totalPages = paginate.pages
        currentPage = paginate.pages
        items = paginate.items

        for pet_info in items:
            response_data['users'].append(pet_info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=200, data=response_data)

    def post(self):
        """
        创建宠物记录
        """
        json_parser = RequestParser()
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('type', required=True, location='json')
        args = json_parser.parse_args()
        name = args.name
        type = args.type

        pet = Pet()
        pet.name = name
        pet.type = type

        response_data = {}

        try:
            db.session.add(pet)
            db.session.commit()
            response_data['petId'] = pet.id
        except Exception as e:
            db.session.rollback()

        return response_to_api(code=200, data=response_data)
