from flask import Flask, render_template, flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flaskmodel.config import *
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
# 创建数据库连接
db = SQLAlchemy(app)

'''
1. 配置数据库
    a. 导入Sqlalchemy扩展
    b. 创建db对象，并配置参数
    c. 终端创建数据库
2. 添加书和作者模型
    a. 继承db.Model
    b. __tablename__：表名
    c. 设置字段名
    d. 设置引用关系
3. 添加数据
4. 使用模板显示数据库查询的数据
    a. 在模板中for循环就行了（我自己试的时候想在py中做，但是没成功）
5. 使用WTF显示表单
    a. 自定义表单类
    b. 模板中显示
    c. secret_key / 编码 / csrf_token的问题
6. 实现相关的增删逻辑
    a. 增加数据
    b. 删除书籍：网页中删除，点击需要发送数据的ID给删除书籍的路由，路由需要接收参数(for else / redirect / url_for 的使用)
    c. 删除作者
'''

# 配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hbb'

# 自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者',validators=[DataRequired()])
    book = StringField('书籍',validators=[DataRequired()])
    submit = SubmitField('提交')

# 添加书和作者模型
class Author(db.Model):
    # 表名
    __tablename__ = 'authors'
    # 字段
    id = db.Column(db.Integer,primary_key = True)
    author_name = db.Column(db.String(16),unique = True)
    books = db.relationship('Book',backref='author')
    # 关系引用
    # books = db.relationship()
    def __repr__ (self):
        return '<Author: %r>' % self.author_name
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String(255),unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    def __repr__ (self):
        return '<Book: %r %r>' % (self.book_name,self.author_id)

#删除作者（记得把书也要删掉）
@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            Book.query.filter_by(author_id = author_id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            flash('删除作者出错')
            db.session.rollback()
    else:
        flash('作者找不到')
    return redirect(url_for('index'))


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            flash('删除书籍出错')
            db.session.rollback()
    else:
        flash('书籍找不到')
    return redirect(url_for('index'))

@app.route('/',methods = ['GET','POST'])
def index():
    # 创建自定义的表单
    author_form = AuthorForm()
    # 查询所有作者信息，让信息传递给模板
    '''
    验证逻辑：
    1. 调用WTF的函数实现验证
    2. 验证通过获取数据
    3. 判断做作者是否存在
    4. 如果作者存在，判断书籍是否存在，没有重复书籍就添加数据，如果重复就提示错误
    5. 如果作者不存在，添加作者与书籍
    6. 验证不通过就提示错误
    '''
    # 1. 调用WTF的函数实现验证
    if author_form.validate_on_submit():
        # 2. 验证通过获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data

        # 3. 判断作者是否存在
        author = Author.query.filter_by(author_name=author_name).first()
        book = Book.query.filter_by(book_name=book_name).first()

        # 4. 如果作者存在
        if author:
            # 判断作者是否存在，没有重复书籍就添加数据，如果重复就提示错误
            if book:
                # 有同名书籍就提示
                flash('已存在同名同作者书籍')
            else:
                # 没有同名书籍，就添加数据
                try:
                    new_book = Book(book_name = book_name,author_id = author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('有作者时添加书籍失败')
                    db.session.rollback() # 如果添加失败就回滚
        else:
            # 如果作者不存在，判断书籍是否存在
            if book:
                # 有同名书籍就提示
                flash('已存在相同的书籍')
            else:
                # 没有同名书籍就添加数据
                try:
                    new_author = Author(author_name=author_name)
                    db.session.add(new_author)
                    db.session.commit()
                    new_book = Book(book_name=book_name, author_id=new_author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('无作者时添加书籍失败')
                    db.session.rollback()  # 如果添加失败就回滚
    else:
        if request.method == 'POST':
            flash('参数不全！')

    authors = Author.query.all()
    return render_template('books.html',authors = authors,form = author_form)

if __name__ == '__main__':
    # db.create_all()
    # db.drop_all()
    # 添加数据
    # au1 = Author(author_name = 'hbb')
    # au2 = Author(author_name = 'ry')
    # au3 = Author(author_name = 'rmf')
    # db.session.add_all([au1,au2,au3])
    # db.session.commit()
    #
    # bk1 = Book(book_name = '量子史话',author_id = au1.id)
    # bk2 = Book(book_name = '我们仨',author_id = au1.id)
    # bk3 = Book(book_name = '管理学',author_id = au2.id)
    # bk4 = Book(book_name = '玩具的学与玩',author_id = au3.id)
    # bk5 = Book(book_name = '教养的迷思',author_id = au3.id)
    # db.session.add_all([bk1,bk2,bk3,bk4,bk5])
    # db.session.commit()

    app.run(debug=True)
