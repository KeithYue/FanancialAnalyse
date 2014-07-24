# coding=utf-8
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
from pymongo import MongoClient
import chartkick

# configuration
DB_HOST = '183.57.42.116'
DB_PORT = '27017'
DB_NAME = 'pingan'
SECRET_KEY = 'development key'
DEBUG = True
TOOL_META = []
TOOL_META.append(dict(name='概况', sub_func=[dict(name='概况1', url='/overview1')]))
TOOL_META.append(dict(name='热度分析', sub_func=[dict(name='热度分析1', url='/hot1')]))
TOOL_META.append(dict(name='相关词分析', sub_func=[dict(name='相关分析1', url='/related1')]))
TOOL_META.append(dict(name='来源分析', sub_func=[dict(name='来源分析1', url='/source1')]))
TOOL_META.append(dict(name='情感分析', sub_func=[dict(name='情感分析1', url='/sentiment1')]))
TOOL_META.append(dict(name='话题分析', sub_func=[dict(name='话题分析1', url='/topic1')]))
KEYWORDS = [
        '平安银行',
        '平安盈',
        '基金智能定投',
        '金橙管家',
        '新一贷',
        '口袋银行'
]

# init the app
app = Flask(__name__)

# load the config file
app.config.from_object(__name__)

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")


def connect_db():
    '''
    connect the database --> the Database instance
    '''
    return MongoClient(app.config.get('DB_HOST'), int(app.config.get('DB_PORT')))


@app.before_request
def before_request():
    g.db = connect_db()
    g.active_tool = None

@app.teardown_request
def teardown_request(exception):
    g.db.disconnect()


@app.route('/')
def hello():
    g.active_tool = None
    return render_template('layout.html')

@app.route('/<function_name>')
def analyse(function_name):
    tools = app.config.get('TOOL_META')
    for t in tools:
        for sub_t in t['sub_func']:
            if function_name == sub_t['url'].split('/')[-1]:
                # invoke the related method
                g.active_tool = (t['name'], sub_t['name'])
                return globals()[function_name]()
    abort(404)
    return

@app.route('/hot1',methods=['POST'])
def hot1():
    product="平安银行"
    product_no = 1
    if request.method == 'POST':
        product = request.form['keyWordsBox']
        product_no += app.config.get('KEYWORDS').index(product)
    data = {}
    f = open("word_count.txt")
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        tmp = line.strip('\n').split(' ')

        if int(tmp[0]) == product_no:
            data[tmp[1]] = int(tmp[2])
    f.close()
    return render_template('hot1.html',data=data, title_t=product)

def related1():
    return render_template('related1.html')

def sentiment1():
    return render_template('sentiment1.html')

def source1():
    return render_template('source1.html')



@app.errorhandler(404)
def page_not_found(error):
    return '404', 404


if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG'))
