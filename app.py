
from flask import Flask, render_template, request, redirect, \
                  url_for
from ckc00util import do_query, do_name_query

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/db2')
def name_query():
    name = request.args.get('name')

    if not name:
        return redirect(url_for('index'))
    header = 'id,city,state,latitude,longitude\n'
    return header + do_name_query(name)

@app.route('/db')
def print_data():
    sex = request.args.get('sex')
    clss = request.args.get('class')

    if not sex or not clss:
        return redirect(url_for('index'))

    header = 'id,city,state,latitude,longitude\n'
    return header + do_query(sex, clss)

if __name__ == '__main__':
    app.run(debug=True)
