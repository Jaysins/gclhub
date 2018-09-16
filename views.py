from flask import Flask, render_template, request, url_for, json, jsonify
from models import User, History, Account
from app import app, db


@app.route('/')
def index():
    """
    index
    """
    return render_template('index.html')


@app.route('/signup')
def signup():
    """
    Signup
    """
    if request.method == 'POST':
        return
    return render_template('signup.html')


@app.route('/login')
def login():
    """
    login
    """
    if request.method == 'POST':
        return
    return render_template('login.html')


# :Todo account page=history payments, if subscribed, else


@app.route('/dashboard')
def dashboard():
    user = User.query.filter_by(id=1).first()
    user_data = {'username': user.name, 'email': user.email}
    check_account = Account.query.filter_by(user_id=1).first()
    history = History.query.filter_by(user_id=1).all()
    return render_template('dashboard.html', user=json.dumps(user_data),
                           subscribed=check_account.plan if check_account is not None else 'None', history=history)


@app.route('/profile')
def profile():
    account = Account.query.filter_by(user_id=1).first()
    return render_template('profile.html', account=account, user=User.query.first().name)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/receive_ref')
def receive_ref():
    data = request.args
    sub = Account(plan=data['plan'].replace('\n', ''),
                  user_id=1, reference=data['reference'])
    db.session.add(sub)
    db.session.commit()
    return jsonify({'response': 'success'})
