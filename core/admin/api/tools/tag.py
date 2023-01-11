from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models.tools import Tag
from common.dao.tools import get_tag_by_id, update_tag_info_by_id, delete_tag_by_args
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.constants import user_constant


class TagResource(Resource):
    """tag列表"""

    def get(self):
        """
        获取文章列表
        :return:
        """
        qs_parser = RequestParser()
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

        if args.type is not None:
            filters.append(Tag.type.like('%' + args.type + '%'))

        order = Tag.id.asc() if _order == 1 else Tag.id.desc()
        try:
            paginate = Tag.query.filter(*filters).order_by(order).paginate(page_num)
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
        json_parser.add_argument('type', required=False, location='json')
        args = json_parser.parse_args()
        type = args.type

        tag = Tag()
        tag.type = type
        response_data = {}
        try:
            db.session.add(tag)
            db.session.commit()
            response_data['TagId'] = tag.id
        except Exception as e:
            db.session.rollback()
        return response_to_api(code=200, data=response_data)

    def delete(self):
        """"
        删除
        """
        json_parser = RequestParser()
        json_parser.add_argument('tagId', type=inputs.positive, required=True, location='json')
        args = json_parser.parse_args()
        tagId = args.tagId
        result = delete_tag_by_args(tagId)
        if result is None:
            return response_to_api(code=4044)
        return response_to_api(code=200)

    def put(self):
        """
        修改
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('tagId', type=inputs.positive, required=True, location='json')
        json_parser.add_argument('type', required=False, location='json')
        args = json_parser.parse_args()

        tagId = args.tagId
        type = args.type

        tag = get_tag_by_id(tagId)
        if tag is None:
            return response_to_api(code=4034)

        update_dict = {}
        if type != None:
            update_dict["type"] = type
        update_tag_info_by_id(tagId, update_dict)
        return response_to_api(code=200)

