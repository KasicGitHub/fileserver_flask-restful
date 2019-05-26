# -*- coding:utf8  -*-
from flask_restful import abort, request
from apps.fileserver.permission import Resource
from flask import send_from_directory
from werkzeug.utils import secure_filename
from apps.fileserver.action import *
from apps.fileserver.models import *
from config import db
from apps.fileserver.permission import login_requiremed

FILE_FOLDER = '/fileserver'


class getFilesOrDownload(Resource):
    def get(self, dirpath=''):
        returnData = {
            'status': 0,
            'message': '',
            'data': {}
        }
        try:
            print(request.path)
            fullpath = os.path.join(FILE_FOLDER, dirpath)

            if os.path.isdir(fullpath):
                file_list = getAllFile(fullpath)

                returnData['status'] = 1
                returnData['data'] = {
                    'file_list': file_list
                }

                return returnData

            if os.path.isfile(fullpath):
                return send_from_directory(FILE_FOLDER, dirpath, as_attachment=True)

            raise Exception('%s: No such file or directory' % dirpath)

        except Exception as error:
            print(error)
            returnData['message'] = str(error)
            return returnData


class uploadFile(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'message': ''
        }
        try:
            print(request.form)
            # path = request.json.get('path')
            path = request.form.get('path')
            f = request.files.get('file')

            if f:
            # if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
                fname = secure_filename(f.filename)  # 中文处理异常
                # fname = f.filename
                print(fname)

                if path:
                    if path[:1] == '/':
                        path = path[1:]
                    filefullpath = os.path.join(FILE_FOLDER, path, fname)
                else:
                    filefullpath = os.path.join(FILE_FOLDER, fname)

                if os.path.exists(filefullpath):
                    raise Exception('%s:file already exists' % fname)

                f.save(filefullpath)  # 保存文件到upload目录
                # token = base64.b64encode(new_filename)
                # print token
                returnData['status'] = 1
                returnData['message'] = 'success'
                return returnData

            raise Exception('check the upload file')

        except Exception as error:
            print(error)
            returnData['message'] = str(error)
            return returnData


class createFolder(Resource):
    def get(self):
        returnData = {
            'status': 0,
            'message': ''
        }
        try:
            folder = request.args.get('folder')
            if folder:
                if folder[:1] == '/':
                    folder = folder[1:]
                folderFullPath = os.path.join(FILE_FOLDER, folder)

                if not os.path.exists(folderFullPath):
                    os.mkdir(folderFullPath)

                    returnData['status'] = 1
                    returnData['message'] = 'success'
                    return returnData

                raise Exception("cannot create directory '%s': File exists" % folderFullPath)

            raise Exception('missing params: folder')

        except Exception as error:
            print(error)
            returnData['message'] = str(error)
            return returnData


class deleteFile(Resource):
    def get(self):
        returnData = {
            'status': 0,
            'message': ''
        }
        try:
            filename = request.args.get('filename')
            if filename:
                if filename[:1] == '/':
                    filename = filename[1:]
                fileFullPath = os.path.join(FILE_FOLDER, filename)

                if not os.path.exists(fileFullPath):
                    raise Exception('%s: No such file or directory' % fileFullPath)

                if os.path.isdir(fileFullPath):
                    os.rmdir(fileFullPath)

                    returnData['status'] = 1
                    returnData['message'] = 'success'
                    return returnData

                else:
                    os.remove(fileFullPath)

                    returnData['status'] = 1
                    returnData['message'] = 'success'
                    return returnData

            raise Exception('missing params: filename')

        except Exception as error:
            print(error)
            returnData['message'] = str(error)
            return returnData


class downloadFile(Resource):
    def get(self, filepath=None):
        print(filepath)
        if filepath and os.path.isfile(os.path.join(FILE_FOLDER, filepath)):
            return send_from_directory(FILE_FOLDER, filepath, as_attachment=True)
        abort(404)


class getUser(Resource):
    def get(self):
        result = []
        querys = User.query.all()

        for query in querys:
            result.append(query.to_json())

        return result


class register(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'message': ''
        }
        try:
            username = request.json.get('username')
            password = request.json.get('password')

            if not username or not password:
                raise Exception('username or password empty')

            user = User.query.filter_by(username=username).first()
            if not user:
                newUser = User()
                newUser.username = username
                newUser.password = password

                db.session.add(newUser)
                db.session.commit()

                token = newUser.generate_auth_token()
                token = str(token, encoding = "utf8")
                print(token)

                returnData['data'] = {
                    'UserId': newUser.id,
                    'Token': token
                }
                return returnData

            raise Exception('user exists')

        except Exception as error:
            print(error)
            returnData['message'] = str(error)
            return returnData


class login(Resource):
    def post(self):
        returnData = {
            'status': 0,
            'code': 200,
            'message': ''
        }
        # try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            raise Exception('username or password empty')

        user = login_requiremed(username, password)

        token = user.generate_auth_token()
        token = str(token, encoding="utf8")
        print(token)

        returnData['status'] = 1
        returnData['data'] = {
            'UserId': user.id,
            'Token': token
        }
        return returnData

        # except Exception as error:
        #     print(error)
        #     returnData['message'] = str(error)
        #     return returnData

