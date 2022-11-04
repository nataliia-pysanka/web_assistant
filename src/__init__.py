from flask import render_template, request, redirect, url_for, session, \
    make_response
from flask import Flask
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

from config import config
import uuid

from src import models
from src.db import db
from src.repository import users_repr, contacts_repr, notes_repr
from datetime import datetime, timedelta


app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)
migrate = Migrate(app, db)

seeder = FlaskSeeder()
seeder.init_app(app, db)


@app.before_request
def before_func():
    auth = True if 'username' in session else False
    if not auth:
        token_user = request.cookies.get('user')
        if token_user:
            user = users_repr.get_user_by_token(token_user)
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

        user = users_repr.login(email, password)
        if user is None:
            return redirect(url_for('login'))

        session['user'] = {'email': user.email, 'id': user.id}
        response = make_response(redirect(url_for('index')))

        if remember:
            token = str(uuid.uuid4())
            expire_date = datetime.now() + timedelta(days=10)
            response.set_cookie('user', token, expires=expire_date)
            users_repr.set_token(user, token)

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
        user = users_repr.create_user(email, password)
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
        user = users_repr.get_user_by_id(user_id)
        users_repr.set_token(user, '')
    session.pop('user')
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', '', expires=-1)

    return response


@app.route('/contacts', strict_slashes=False)
def contacts():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))

    user_id = session.get('user', {}).get('id')
    page = request.args.get('page', 1, type=int)

    contacts_list = contacts_repr.get_contacts(user_id=user_id, page=page)

    return render_template('pages/contacts.html',
                           auth=auth,
                           contacts=contacts_list)


@app.route('/contact/<int:contact_id>', strict_slashes=False)
def contact(contact_id):
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))

    contact_info = contacts_repr.get_contact_by_id(contact_id=contact_id)

    return render_template('pages/contact.html',
                           auth=auth, contact=contact_info)


@app.route('/notes', strict_slashes=False)
def notes():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))

    user_id = session.get('user', {}).get('id')
    page = request.args.get('page', 1, type=int)

    notes_list = notes_repr.get_notes(user_id=user_id, page=page)

    return render_template('pages/notes.html',
                           auth=auth,
                           notes=notes_list)


@app.route('/note/<int:note_id>', strict_slashes=False)
def note(note_id):
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))

    note_info = notes_repr.get_note_by_id(note_id=note_id)

    return render_template('pages/note.html',
                           auth=auth, note=note_info)


@app.route('/note/search', strict_slashes=False)
def note_search():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))

    user_id = session.get('user', {}).get('id')
    page = request.args.get('page', 1, type=int)
    tag_name = request.args.get('tag').split(',')

    note_info = notes_repr.get_notes_by_tag(user_id=user_id,
                                            tag_name=tag_name,
                                            page=page)

    return render_template('pages/notes.html',
                           auth=auth, notes=note_info)


@app.route('/contacts/add', methods=['GET', 'POST'], strict_slashes=False)
def contact_add():
    auth = True if 'user' in session else False
    if not auth:
        return redirect(url_for('index'))

    groups = contacts_repr.get_groups()

    if request.method == 'POST':
        user_id = session.get('user', {}).get('id')
        contact_data = {'user_id': user_id,
                        'first_name': request.form.get('first-name'),
                        'last_name': request.form.get('last-name')}

        if request.form.get('adress'):
            contact_data.update({'adress': request.form.get('adress')})

        phones = []
        for num in range(4):
            if request.form.get('phone_' + str(num)):
                phones.append(request.form.get('phone_' + str(num)))
        if phones:
            contact_data.update({'phones': phones})

        emails = []
        for num in range(4):
            if request.form.get('email_' + str(num)):
                emails.append(request.form.get('email_' + str(num)))
        if emails:
            contact_data.update({'emails': emails})

        groups = []
        if request.form.get('group') != 'None':
            gr_name = request.form.get('group')
            groups.append(contacts_repr.get_group_by_name(gr_name))

        if groups:
            contact_data.update({'groups': groups})

        if request.form.get('birthday'):
            request.form.get('birthday')
            contact_data.update({'birth': request.form.get('birthday')})

        contact_new = contacts_repr.create_contact(**contact_data)
        if contact_new:
            return redirect(url_for(f'contact', contact_id=contact_new.id))

    return render_template('pages/contact_add.html',
                           auth=auth, groups=groups)
