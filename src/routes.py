from flask import render_template, request
from src import app


@app.route('/healthcheck')
def healthcheck():
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    auth = True
    if request.method == 'POST':
        if request.form.get('contacts_input'):
            return render_template('pages/contacts.html', auth=auth)
        elif request.form.get('notes_input'):
            return render_template('pages/notes.html', auth=auth)

    return render_template('pages/index.html', auth=auth)


@app.route('/login', strict_slashes=False)
def login():
    return render_template('pages/login.html')


@app.route('/signin', strict_slashes=False)
def signin():
    return render_template('pages/signin.html')


@app.route('/logout', strict_slashes=False)
def logout():
    return render_template('index.html')


@app.route('/contacts', strict_slashes=False)
def contacts():
    return render_template('pages/contacts.html')


@app.route('/notes', strict_slashes=False)
def notes():
    return render_template('pages/notes.html')
