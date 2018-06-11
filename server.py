import re
import json, requests
from pprint import pprint
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_all_likes_for, get_show_ids_liked, _unlike, create__like, create_user, get_user_by_id, get_user_by_email, get_user_by_name, create_user


EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

app = Flask(__name__)
app.secret_key = '0d599f0ec05c3bda8c3b8a68c32a1b47'

ApiUrl = 'http://api.tvmaze.com'

def get_request(url):
    response = requests.get(url)
    return json.loads(response.text)

@app.route('/')
def index():
    if session:
        likes = get_all_likes_for(session['user_id'])
        show_liked = []
        for l in likes:
            url = '{}/shows/{}'.format(ApiUrl, l.show_id)
            show = get_request(url)
            show_liked.append({'show': show})
        return render_template('index.html', shows = show_liked, show_id_liked = get_show_ids_liked(session['user_id']))
    else:
        return render_template('index.html')


@app.route('/search-redirect')
def search_redirect():
    return redirect(url_for('search', query=request.args['html_query']))

@app.route('/search/<query>')
def search(query):
    url = '{}/search/shows?q={}'.format(ApiUrl, query)
    shows = get_request(url)
    if session:
        show_id_liked = get_show_ids_liked(session['user_id'])
    else:
        show_id_liked = []
    return render_template('index.html', shows = shows, show_id_liked = show_id_liked, destination = (request.url).replace('/', '||'))

@app.route('/create-like/<show_id>/<destination>')
def create_like(show_id, destination):
    create__like(session['user_id'], show_id)
    return redirect(destination.replace('||', '/'))

@app.route('/unlike/<show_id>/<destination>')
def unlike(show_id, destination):
    _unlike(session['user_id'], show_id)

    if destination != '_':
        return redirect(destination.replace('||', '/'))
    else:
        return redirect(url_for('index'))

def is_blank(name, field):
    if len(field) == 0:
        flash('{} cant be blank'.format(name))
        return True
    return False

@app.route('/login-form')
def login_form():
    return render_template('login.html')

@app.route('/register-form')
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['html_fullname']
    username = request.form['html_username']
    email = request.form['html_email']
    password = request.form['html_password']
    confirm = request.form['html_confirm']

    is_valid = not is_blank('fullname', fullname)
    is_valid = not is_blank('email', email)
    is_valid = not is_blank('password', password)
    is_valid = not is_blank('confirm', confirm)

    if not EMAIL_REGEX.match(email):
        is_valid = False
        flash('invalid email format')

    if password != confirm:
        is_valid = False
        flash('password did not match')
    
    if(len(password) < 6):
        is_valid = False
        flash('password is too short')    

    if is_valid:
        try:
            user = create_user(fullname, username, email, password)
            setup_web_session(user)
            return redirect(url_for('index'))
        except:
            flash('email already registered.')

    return redirect(url_for('register_form'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['html_email']
    password = request.form['html_password']

    try:
        user = get_user_by_email(email)
        if user.password == password:
            setup_web_session(user)
            return redirect(url_for('index'))
        else:
            flash('password do not match')
    except:
        flash('invalid login')

    return redirect(url_for('login_form'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def setup_web_session(user):
    session['user_id'] = user.id
    session['username'] = user.username
    return True


app.run(debug=True)