from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from redis import StrictRedis

from flask_wtf import CSRFProtect

from config import config_dict

from flask_session import Session

import logging

from logging.handlers import RotatingFileHandler

from config import config_dict

from info.module.index import index_db

def create_log(config_name):

    """记录日志的配置信息"""

    # 设置日志的记录等级
    # config_dict[config_name].LOG_LEVEL获得日志记录等级
    logging.basicConfig(level=config_dict[config_name].LOG_LEVEL)  # 调试debug级

    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)

    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    # INFO：manager.py ：18 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)

    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

# 工厂方法，根据传入的不同的配置信息，创建不同的app
def create_app(config_name): #development-开发环境的app对象 production就是生产模式的appp

    # 0.调用日志方法
    create_log(config_name)

    # 创建app对象
    app = Flask(__name__)

    # 注册配置信息到app中

    # config_dict["development"]--->DevelopmentConfig
    # config_dict["producttion"]--->ProductionConfig
    config_class = config_dict[config_name]

    app.config.from_object(config_class)

    # 创建数据库对象
    db = SQLAlchemy(app)

    # 创建redis数据库对象
    redis_store = StrictRedis(host=config_class.REDIS_HOST,

                              port=config_class.REDIS_PORT,

                              db=config_class.REDIS_NUM, )

    # 开启flask后端csrf验证保护机制

    csrf = CSRFProtect(app)

    # 借助第三方session类去调整flask中的session存储位置

    # flask_session的配置信息

    Session(app)

    app.register_blueprint(index_db)

    return app
