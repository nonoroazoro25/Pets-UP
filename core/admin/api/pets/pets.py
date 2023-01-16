from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.constants import user_constant
from common.models.pets import Pet
from common.dao.pets import get_pet_by_user_id, delete_pet_by_pet_id, update_pet_name_by_pet_id
from common.utils.response_util import response_to_api
from common.models import db


class PetsResource(Resource):
    """
    宠物（没用）
    """

    def get(self):
        """
        宠物列表
        :return:
        """
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
        response_data['details'] = []
        filters = []

        if args.name is not None:
            filters.append(Pet.name.like('%' + args.name + '%'))
        if args.type is not None:
            filters.append(Pet.type.like('%' + args.type + '%'))

        order = Pet.id.asc() if _order == 1 else Pet.id.desc()
        try:
            paginate = Pet.query.filter(*filters).order_by(order).paginate(page_num)
        except Exception as e:
            print('some error happen %s', e)

        totalPages = paginate.pages
        currentPage = paginate.pages
        items = paginate.items

        for pet_info in items:
            response_data['details'].append(pet_info.to_basic_dict())

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
        json_parser.add_argument('user_id', required=True, location='json')
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('type', required=True, location='json')
        json_parser.add_argument('photo', required=False, location='json')
        args = json_parser.parse_args()
        name = args.name
        type = args.type
        userId = args.user_id

        pet = Pet()
        pet.name = name
        pet.type = type
        pet.user_id = userId

        response_data = {}

        try:
            db.session.add(pet)
            db.session.commit()
            response_data['petId'] = pet.id
        except Exception as e:
            db.session.rollback()

        return response_to_api(code=200, data=response_data)

    def delete(self):
        """"
        删除
        """
        json_parser = RequestParser()
        json_parser.add_argument('petId', type=inputs.positive, required=True, location='json')
        args = json_parser.parse_args()
        petId = args.petId
        result = delete_pet_by_pet_id(petId)
        if result is None:
            return response_to_api(code=4044)
        return response_to_api(code=200)

    def put(self):
        """
        修改
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('pet_id', type=inputs.positive, required=True, location='json')
        json_parser.add_argument('user_id', required=False, location='json')
        json_parser.add_argument('name', required=False, location='json')
        json_parser.add_argument('type', required=False, location='json')
        args = json_parser.parse_args()

        pet_id = args.pet_id
        user_id = args.user_id
        name = args.name
        type = args.type

        pet = get_pet_by_user_id(pet_id)
        if pet is None:
            return response_to_api(code=4034)

        update_dict = {}
        if user_id != None:
            update_dict["user_id"] = user_id
        if name != None:
            update_dict["name"] = name
        if type != None:
            update_dict["type"] = type
        update_pet_name_by_pet_id(pet_id, update_dict)
        return response_to_api(code=200)




