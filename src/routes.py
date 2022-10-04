from flask import render_template, request, redirect, url_for
from src import app
from src.repository import users


@app.route('/healthcheck')
def healthcheck():
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    if request.method == 'POST':
        if request.form.get('contacts_input'):
            return redirect(url_for('contacts'))
        elif request.form.get('notes_input'):
            return redirect(url_for('notes'))

    return render_template('pages/index.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.login(email, password)
        if user is None:
            return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route('/signin', methods=['GET', 'POST'], strict_slashes=False)
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.create_user(email, password)
        return redirect(url_for('index'))
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
