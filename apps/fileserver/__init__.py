# -*- coding:utf8  -*-
from flask_restful import Api
from apps.fileserver.views import *

def regist_fileserver(app):
    api = Api(app)
    api.add_resource(login, '/login')
    api.add_resource(createFolder, '/create')
    api.add_resource(uploadFile, '/upload')
    # api.add_resource(downloadFile, '/download/<path:filepath>')
    api.add_resource(deleteFile, '/delete')

    api.add_resource(register, '/register')
    api.add_resource(getUser, '/getUser')

    api.add_resource(getFilesOrDownload, '/', '/<path:dirpath>')

