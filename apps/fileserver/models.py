# -*- coding:utf8  -*-
from config import app, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    hashpass = db.Column(db.String(150), unique=True, nullable=False)
    roleid = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    # property:将装饰器的方法提升为类属性--->默认为getter方法--->解耦
    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    # 定义一个赋值的方法
    @password.setter
    def password(self, value):
        self.hashpass = generate_password_hash(value)

    # 定义一个验证密码的方法
    def check_password(self, password):
        return check_password_hash(self.hashpass, password)

    # 生成token
    def generate_auth_token(self, expiration=app.config['TOKEN_TIMEOUT']):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # token校验
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            raise Exception('token expired', 50014)
            # return None, message  # valid token, but expired
        except BadSignature:
            raise Exception('invalid token', 50008)
            # return None, message  # invalid token
        user = User.query.get(data['id'])
        if user:
            return user

        raise Exception('user not exists', 405)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username
        }


class Role(db.Model):   # 角色表
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50), unique=True, nullable=False)


class RolePermission(db.Model):     # 角色权限表
    id = db.Column(db.Integer, primary_key=True)
    roleid = db.Column(db.Integer, nullable=False, index=True)
    endpoint = db.Column(db.String(50), unique=True, nullable=False)
    read = db.Column(db.Boolean, default=True, nullable=False)
    write = db.Column(db.Boolean, default=False, nullable=False)


class OpenInterface(db.Model):     # 接口开放表
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(50), unique=True, nullable=False, index=True)
    open = db.Column(db.Boolean, default=True, nullable=False)


db.create_all()
