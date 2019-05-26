# from flask import Flask
from apps.fileserver import regist_fileserver
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
from config import app

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# db = SQLAlchemy(app)

def init_app(app):
    regist_fileserver(app)

init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9528', debug=True, threaded=True)
