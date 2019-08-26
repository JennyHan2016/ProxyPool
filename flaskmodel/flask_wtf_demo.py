from flask import request,Flask,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  DataRequired,EqualTo


app = Flask(__name__)
app.secret_key = 'hbb'

# 使用WTF实现表单，自定义表单类
class LoginForm(FlaskForm):
    username = StringField(u'用户名：',validators=[DataRequired()])
    password = PasswordField(u'密码：',validators=[DataRequired()])
    password2 = PasswordField(u'确认密码：',validators=[DataRequired(),EqualTo('password','密码填充不一致')])
    submit = SubmitField(u'提交')
@app.route('/',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    # 1. 判断请求方式
    if request.method == 'POST':
        # 2.获取请求的参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 3. 验证逻辑，wtf可以一句话实现校验
        # 4. 我们没有CSRF token（这个在模板中添）
        if login_form.validate_on_submit():
            print(username)
            return 'success'
        else:
            flash('参数错误')
    return render_template('loginForm.html',form=login_form)


# 用普通的方法实现：
# @app.route('/',methods=['GET','POST'])
# def index():
#     # request:请求对象，获取请求方式、数据
#     # 实现一个简单的逻辑处理
#     # 1. 路由需要有get和post两种请求 ，需要判断请求方式
#     # 2. 获取请求的参数
#     # 3. 判断逻辑：是否填写，密码是否相同
#     # 4. 如果没有问题，就返回success
#     # 5. 模板中需要遍历flash消息（flash需要对消息加密，设置secret_key,做加密消息的混淆）
#     if request.method == 'POST':
#         # 获取请求参数
#         username = request.form.get('username')
#         password = request.form.get('password')
#         password2 = request.form.get('password2')
#         # 判断参数是否都填写
#         if not all([username,password,password2]):
#             # print('参数不完整')
#             flash(u'参数不完整')
#         elif password != password2:
#             # print('密码不一致')
#             flash(u'密码不一致')
#         else:
#             return 'success'
#
#     return render_template('loginForm.html')


if __name__ == '__main__':
    app.run(debug=True)