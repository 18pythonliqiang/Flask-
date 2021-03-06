
# class Person(object):
#
#     def __eq__(self, other):
#         return "ssad"
#
#     def __init__(self):
#         self.password_hash = ""
#
#     @property
#     def password(self):
#         print("getter 方法被触发了")
#
#     @password.setter
#     def password(self, value):
#         # 加密
#         print("setter方法被触发了 %s" %value)
#
# if __name__ == '__main__':
#     p = Person()
#     p1 = Person()
#     p.password = "1234"
#     print(p == p1)

    # print(p.password)

# -------------------------------------------

# import functools
#
# def login_user_data(view_func):
#
#     @functools.wraps(view_func)
#     def wrapper(*args, **kwargs):
#
#         return view_func(*args, **kwargs)
#
#     return wrapper
#
#
# @login_user_data
# def index():
#     """注释"""
#     print("inex")
#
# @login_user_data
# def hello():
#     print("hello")
#
# if __name__ == '__main__':
#     print(index.__name__)
#     print(hello.__name__)

# -------------------------------------------
import datetime
import random
from info import db
from info.models import User
from manage import app


def add_test_users():
    users = []
    # 获取当前时间
    now = datetime.datetime.now()
    for num in range(0, 10000):
        try:
            user = User()
            user.nick_name = "%011d" % num
            user.mobile = "%011d" % num
            user.password_hash = "pbkdf2:sha256:50000$SgZPAbEj$a253b9220b7a916e03bf27119d401c48ff4a1c81d7e00644e0aaf6f3a8c55829"
            # 最后一次登录时间 时间范围：31号-1号之间随机一个时间作为登录时间
            user.last_login = now - datetime.timedelta(seconds=random.randint(0, 2678400))
            users.append(user)
            print(user.mobile)
        except Exception as e:
            print(e)
    # 开启应用上下文
    with app.app_context():
        db.session.add_all(users)
        db.session.commit()
    print("ok")

if __name__ == '__main__':
    add_test_users()












