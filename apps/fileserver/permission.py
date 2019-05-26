# -*- coding:utf8  -*-
import flask_restful
from flask_restful import request
from functools import wraps
from apps.fileserver.models import *


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        returnData = {
            'status': 0,
            'code': 403,
            'message': ''
        }
        try:
            # host = request.remote_addr  # 请求源IP

            endpoint = request.endpoint  # 接口
            print('接口:', endpoint)
            if endpoint and check_open_interface(endpoint):  # 检查请求接口是否为开放接口
                return func(*args, **kwargs)

            header = request.headers
            token = header.get('Token')
            if not token:   # 请求没带Token拒绝执行
                raise Exception('Privilege Validation Failed', 50009)

            user = check_token(token)   # 检查Token合法
            if user.id == 1:    # 超级管理员跳过接口权限检查
                return func(*args, **kwargs)

            permission_list = get_user_permission(user)  # 获取用户接口权限
            if endpoint in permission_list:  # 检查用户接口权限
                return func(*args, **kwargs)

            raise Exception('Users do not have access to this interface', 403)

        except Exception as error:
            message = error.args[0]
            if len(error.args) > 1:
                code = error.args[1]
                returnData['code'] = code
            returnData['message'] = str(message)
            return returnData
    return wrapper


class Resource(flask_restful.Resource):  # Resource类继承,增加权限校验方法
    method_decorators = [authenticate]   # applies to all inherited resources


def login_requiremed(username, password):   # 登录校验
    user = User.query.filter_by(username=username).first()
    if not user:
        raise Exception('user not exists', 401)

    if user.check_password(password):
        return user

    raise Exception('invalid password', 401)


def check_token(token): # 检查Token是否合法
    return User.verify_auth_token(token)


def check_open_interface(endpoint): # 检查访问接口是否为开放接口
    rp = OpenInterface.query.filter(OpenInterface.endpoint == endpoint, OpenInterface.open == 1).first()

    if rp:
        return True

    return False


def get_user_permission(user):  # 检查用户角色权限
    permission_list = []
    if not user.roleid:
        return permission_list

    role = Role.query.get(user.roleid)
    if not role:
        raise Exception('Error in user role setting')

    querys = RolePermission.query.filter_by(roleid=role.id).all()

    for pm in querys:
        permission_list.append(pm.endpoint)

    return permission_list
