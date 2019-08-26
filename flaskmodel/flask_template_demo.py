from flask import Flask,render_template

app = Flask(__name__) # type:Flask

@app.route('/')
def index():
    my_int = 10
    my_dic = {
        'name':'hanbingbing',
        'adress':'jiading'
    }
    my_list = [98,55,25,102542]
    url_str = 'www.baidu.com'
    return render_template('index.html',
                           url_str = url_str,
                           my_list = my_list,
                           my_dic = my_dic,
                           my_int = my_int)
if __name__ == '__main__':
    app.run(debug=True)
