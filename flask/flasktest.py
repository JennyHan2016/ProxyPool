from flask import Flask

app = Flask(__name__)
@app.route('/get_order/<order_id>')
def hello_world(order_id):
     return '客户id是： ' + order_id
if __name__ == '__main__':
    app.run()