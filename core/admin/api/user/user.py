from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.utils.param_verify import verify_int_type
from common.models.user import User
from common.dao.user import get_user_by_user_id, update_user_by_user_id, delete_user_by_user_id
from common.models import db
from common.constants import user_constant
from flask import current_app, g
from common.utils.response_util import response_to_api


class UserResource(Resource):

    def get(self):
        """
        获取用户列表
        查询用户
        :return:
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('account', required=False, type=verify_int_type, location='args')
        qs_parser.add_argument('email', required=False, location='args')
        qs_parser.add_argument('status', required=False, location='args')
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

        if args.account is not None:
            filters.append(User.account.like('%' + args.account + '%'))
        if args.email is not None:
            filters.append(User.email.like('%' + args.email + '%'))

        order = User.id.asc() if _order == 1 else User.id.desc()
        try:
            paginate = User.query.filter(*filters).order_by(order).paginate(page_num, page_count, False)
        except Exception as e:
            current_app.logger.error(e)
            return response_to_api(code=1001)

        totalPages = paginate.pages
        currentPage = paginate.page
        items = paginate.items

        # get user info
        for user_info in items:
            response_data['users'].append(user_info.to_basic_dict())

        response_data['current'] = currentPage
        response_data['pages'] = totalPages
        response_data['size'] = page_count
        response_data['total'] = paginate.total
        return response_to_api(code=200, data=response_data)

    def post(self):
        """
        创建用户
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('account', required=True, location='json')
        json_parser.add_argument('passwd', required=True, location='json')
        json_parser.add_argument('email', required=True, location='json')
        args = json_parser.parse_args()
        account = args.account
        passwd = args.passwd
        email = args.email

        user = User()
        user.account = account
        user.password = passwd
        user.email = email
        response_data = {}
        try:
            db.session.add(user)
            db.session.commit()
            response_data['UserId'] = user.id
        except Exception as e:
            db.session.rollback()
        return response_to_api(code=200, data=response_data)

    def put(self):
        """
        更新用户信息
        :return:
        """
        json_parser = RequestParser()
        json_parser.add_argument('userId', type=inputs.positive, required=True, location='json')
        json_parser.add_argument('account', required=False, location='json')
        json_parser.add_argument('password', required=False, location='json')
        json_parser.add_argument('email', required=False, location='json')
        json_parser.add_argument('status', required=False, location='json')
        json_parser.add_argument('pet_ids', required=False, location='json')
        args = json_parser.parse_args()

        userId = args.userId
        account = args.account
        password = args.password
        email = args.email
        status = args.status
        pet_ids = args.pet_ids

        user = get_user_by_user_id(userId)
        if user is None:
            return response_to_api(code=4034)

        update_dict = {}
        if account != None:
            update_dict["account"] = account
        if password != None:
            update_dict["password"] = password
        if email != None:
            update_dict["email"] = email
        if status != None:
            update_dict["status"] = status
        if pet_ids != None:
            update_dict["pet_ids"] = pet_ids
        update_user_by_user_id(userId, update_dict)
        return response_to_api(code=200)

    def delete(self):
        """"
        删除用户
        """
        json_parser = RequestParser()
        json_parser.add_argument('userId', type=inputs.positive, required=True, location='json')
        args = json_parser.parse_args()
        userId = args.userId
        result = delete_user_by_user_id(userId)
        if result is None:
            return response_to_api(code=4044)
        return response_to_api(code=200)


