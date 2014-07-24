# coding=utf-8
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from pymongo import MongoClient
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

# init the app
app = Flask(__name__)

# load the config file
app.config.from_object(__name__)



def connect_db():
    '''
    connect the database --> the Database instance
    '''
    return MongoClient(app.config.get('DB_HOST'), int(app.config.get('DB_PORT')))


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.disconnect()


@app.route('/')
def hello():
    return render_template('layout.html', active_tool=None)

@app.route('/<function_name>')
def analyse(function_name):
    tools = app.config.get('TOOL_META')
    for t in tools:
        for sub_t in t['sub_func']:
            if function_name == sub_t['url'].split('/')[-1]:
                return render_template(sub_t['url'].split('/')[-1]+'.html', active_tool=(t['name'], sub_t['name']))
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return '404', 404


if __name__ == '__main__':
    print(globals())
    app.run(debug=app.config.get('DEBUG'))
