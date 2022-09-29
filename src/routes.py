from flask import render_template
from src import app


@app.route('/healthcheck')
def healthcheck():
    return 'Hello World!'


@app.route('/')
def index():
    auth = False
    return render_template('pages/index.html', title='Personal Assistant!',
                           auth=auth)


@app.route('/login')
def login():
    return render_template('pages/login.html')
