from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()


app = Flask(__name__)

# 配置数据库的地址
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root123'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'flask_sql_demo'

app.config['SQLALCHEMY_DATABASE_URI'] = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

# 跟踪数据库的修改：不建议开启，未来的版本中会移除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
两张表
角色（管理员 / 普通用户）
用户（角色ID / ）
'''
# 数据库的模型，需要继承db.Model
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义字段
    # db.Column表示是一个字段
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16))
    user = db.relationship('User',backref = 'role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16))
    email = db.Column(db.String(32))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id')) # 外键 表名.id

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/')
def index():
    return 'hello world!'

if __name__ == '__main__':
    users = User.query.all()
    for user in users:
        print(user.role.id)

    # roles = Role.query.all()
    # for role in roles:
    #     for user in role.user:
    #         print(role.name,user,user.email)


    # for user in users:
    #     print(user)
    # db.create_all()
    # role1 = Role(id = 1,name = 'admin')
    # role2 = Role(id = 2,name = 'guest')
    # db.session.add(role1)
    # db.session.add(role2)
    # user1 = User(name='hbb', email='hbb@126.com', role_id=role1.id)
    # user2 = User(name='ry', email='ry@126.com', role_id=role2.id)
    # user3 = User(name='rmf', email='rmf@126.com', role_id=role2.id)
    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.add(user3)
    # db.session.add_all([user1,user2,user3])
    # db.session.commit()
    # db.drop_all()
    # users = User.query.all()
    # for user in users:
    #     print(user.name,user.role.name)
    # role = Role.query.get(14)
    # print(role)
    # print(role.user)