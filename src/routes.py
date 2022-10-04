from flask import render_template, request, redirect, url_for, session, \
    make_response
import uuid
from src import app
from src.repository import users
from datetime import datetime, timedelta


@app.before_request
def before_func():
    auth = True if 'username' in session else False
    if not auth:
        token_user = request.cookies.get('user')
        if token_user:
            user = users.get_user_by_token(token_user)
            if user:
                session['user'] = {'email': user.email, 'id': user.id}


@app.route('/healthcheck')
def healthcheck():
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    auth = True if 'user' in session else False
    if request.method == 'POST':
        if request.form.get('contacts_input'):
            return redirect(url_for('contacts'))
        elif request.form.get('notes_input'):
            return redirect(url_for('notes'))

    return render_template('pages/index.html', auth=auth)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    auth = True if 'user' in session else False
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = users.login(email, password)
        if user is None:
            return redirect(url_for('login'))

        session['user'] = {'email': user.email, 'id': user.id}
        response = make_response(redirect(url_for('index')))

        if remember:
            token = str(uuid.uuid4())
            expire_date = datetime.now() + timedelta(days=10)
            response.set_cookie('user', token, expires=expire_date)
            users.set_token(user, token)

        return response
    if auth:
        return redirect(url_for('index'))
    return render_template('pages/login.html')


@app.route('/signin', methods=['GET', 'POST'], strict_slashes=False)
def signin():
    auth = True if 'user' in session else False
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.create_user(email, password)
        return redirect(url_for('index'))
    if auth:
        return redirect(url_for('index'))
    return render_template('pages/signin.html')


@app.route('/logout', strict_slashes=False)
def logout():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(request.url)

    user_id = session.get('user', {}).get('id')
    if user_id:
        user = users.get_user_by_id(user_id)
        users.set_token(user, '')
    session.pop('user')
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', '', expires=-1)

    return response


@app.route('/contacts', strict_slashes=False)
def contacts():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))
    return render_template('pages/contacts.html', auth=auth)


@app.route('/notes', strict_slashes=False)
def notes():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))
    return render_template('pages/notes.html', auth=auth)
