from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models.recipe import RawMaterial
from common.dao.material import delete_material_by_args, update_material_info_by_id, get_material_by_id
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.constants import user_constant


class MaterialResource(Resource):
    """食材"""

    def get(self):
        qs_parser = RequestParser()
        qs_parser.add_argument('name', required=False, location='args')
        qs_parser.add_argument('nutrient_content', required=False, location='args')
        qs_parser.add_argument('matchable', required=False, location='args')
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
            filters.append(RawMaterial.name.like('%' + args.name + '%'))

        order = RawMaterial.id.asc() if _order == 1 else RawMaterial.id.desc()
        try:
            paginate = RawMaterial.query.filter(*filters).order_by(order).paginate(page_num)
        except Exception as e:
            print('some error happen %s', e)

        totalPages = paginate.pages
        currentPage = paginate.pages
        items = paginate.items

        for material_info in items:
            response_data['details'].append(material_info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=200, data=response_data)

    def post(self):
        """
        创建原料
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('nutrient_content', required=False, location='json')
        json_parser.add_argument('matchable', required=False, location='json')
        args = json_parser.parse_args()
        name = args.name
        nutrient_content = args.nutrient_content
        matchable = args.matchable

        material = RawMaterial()
        material.name = name
        material.nutrient_content = nutrient_content
        material.matchable = matchable
        response_data = {}
        try:
            db.session.add(material)
            db.session.commit()
            response_data['MaterialId'] = material.id
        except Exception as e:
            db.session.rollback()
        return response_to_api(code=200, data=response_data)

    def delete(self):
        """"
        删除
        """
        json_parser = RequestParser()
        json_parser.add_argument('materialId', type=inputs.positive, required=True, location='json')
        args = json_parser.parse_args()
        materialId = args.materialId
        result = delete_material_by_args(materialId)
        if result is None:
            return response_to_api(code=4044)
        return response_to_api(code=200)

    def put(self):
        """
        修改
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('materialId', type=inputs.positive, required=True, location='json')
        json_parser.add_argument('nutrient_content', required=False, location='json')
        json_parser.add_argument('matchable', required=False, location='json')
        args = json_parser.parse_args()

        materialId = args.materialId
        nutrient_content = args.nutrient_content
        matchable = args.matchable

        material = get_material_by_id(materialId)
        if material is None:
            return response_to_api(code=4034)

        update_dict = {}
        if nutrient_content != None:
            update_dict["nutrient_content"] = nutrient_content
        if matchable != None:
            update_dict["matchable"] = matchable
        update_material_info_by_id(materialId, update_dict)
        return response_to_api(code=200)

