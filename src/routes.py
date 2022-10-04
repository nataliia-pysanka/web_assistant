from flask import render_template, request, redirect, url_for, session, \
    make_response
from src import app
from src.repository import users


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
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = users.login(email, password)
        if user is None:
            return redirect(url_for('login'))

        session['user'] = {'email': user.email, "id": user.id}
        response = make_response(redirect(url_for('index')))

        if remember:
            pass

        return response
    return render_template('pages/login.html')


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
    auth = True if 'user' in session else False
    if not auth:
        return redirect(request.url)
    session.pop('user')
    response = make_response(redirect(url_for('index')))
    return response


@app.route('/contacts', strict_slashes=False)
def contacts():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(request.url)
    return render_template('pages/contacts.html', auth=auth)


@app.route('/notes', strict_slashes=False)
def notes():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(request.url)
    return render_template('pages/notes.html', auth=auth)
