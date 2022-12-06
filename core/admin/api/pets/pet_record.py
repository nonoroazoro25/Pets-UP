from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.constants import user_constant
from common.models.pets import PetRecord
from common.utils.response_util import response_to_api
from common.models import db


class PetsRecordResource(Resource):
    """
    宠物日常记录类
    """
    def get(self):
        """
        获取记录列表
        :return:
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('pet_id', required=False, location='args')
        qs_parser.add_argument('tag', required=False, location='args')
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

        if args.pet_id is not None:
            filters.append(PetRecord.pet_id.like('%' + args.pet_id + '%'))
        if args.tag is not None:
            filters.append(PetRecord.tag.like('%' + args.tag + '%'))

        order = PetRecord.id.asc() if _order == 1 else PetRecord.id.desc()
        try:
            paginate = PetRecord.query.filter(*filters).order_by(order).paginate(page_num)
        except Exception as e:
            print('some error happen %s', e)

        totalPages = paginate.pages
        currentPage = paginate.pages
        items = paginate.items

        for pet_record_info in items:
            response_data['details'].append(pet_record_info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=200, data=response_data)

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('pet_id', required=True, location='json')
        json_parser.add_argument('title', required=False, location='json')
        json_parser.add_argument('photo', required=False, location='json')
        json_parser.add_argument('detail', required=False, location='json')
        json_parser.add_argument('weight', required=False, location='json')
        json_parser.add_argument('tag', required=False, location='json')
        args = json_parser.parse_args()
        pet_id = args.pet_id
        title = args.title
        photo = args.photo
        detail = args.detail
        weight = args.weight
        tag = args.tag

        pet_record = PetRecord()
        pet_record.pet_id = pet_id
        pet_record.title = title
        pet_record.photo = photo
        pet_record.detail = detail
        pet_record.weight = weight
        pet_record.tag = tag
        response_data = {}

        try:
            db.session.add(pet_record)
            db.session.commit()
            response_data['petRecordId'] = pet_record.id
        except Exception as e:
            db.session.rollback()

        return response_to_api(code=200, data=response_data)
