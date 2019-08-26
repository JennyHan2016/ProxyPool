from flask import Flask,g
# 2. 创建flask应用程序实例
# 需要传入__name__，作用是为了确定资源所在的路径
app = Flask(__name__)
 # 3. 定义路由及视图函数
 # Flask中定义路由是通过装饰器实现的
 # 路由默认只支持get，如果需要增加，需要自行指定
@app.route('/',methods=['GET','POST'])
def index():
     return 'hello Flask'

 # 使用同一个视图函数，来显示不同用户的订单信息
 # <>定义路由的参数，<>内需要起个名字
@app.route('/order/<int:order_id>')
def get_order(order_id):
     return 'order_id %s' % order_id
 # 参数类型默认是字符串unicode
 # 要对参数作优化，比如说指定参数类型为int类型:在视图函数的()内填入参数名，那么后面的代码才能去使用

 #启动程序
if __name__ == '__main__':
     app.run()