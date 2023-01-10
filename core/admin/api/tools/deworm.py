from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models.tools import Deworm
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.constants import user_constant


class DewormResource(Resource):
    """驱虫列表"""

    def get(self):
        """
        获取驱虫列表
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
        response_data['details'] = []
        filters = []

        order = Deworm.id.asc() if _order == 1 else Deworm.id.desc()
        try:
            paginate = Deworm.query.filter(*filters).order_by(order).paginate(page_num)
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
        创建驱虫记录
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('dose', required=False, location='json')
        json_parser.add_argument('remark', required=True, location='json')
        args = json_parser.parse_args()
        remark = args.remark
        dose = args.dose

        deworm = Deworm()
        deworm.dose = dose
        deworm.remark = remark
        response_data = {}
        try:
            db.session.add(deworm)
            db.session.commit()
            response_data['DewormId'] = deworm.id
        except Exception as e:
            db.session.rollback()
        return response_to_api(code=200, data=response_data)

