from flask import Flask, render_template, request, url_for, json, jsonify, redirect
from models import User, History, Account
from app import app, db, login_manager
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, login_user, current_user
from forms import RegisterForm, LoginForm



@login_manager.user_loader
def load_user(user_id):
    """

    :param user_id:
    :return:
    """
    # noinspection PyUnresolvedReferences
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """
    index
    """
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup
    """
    form = RegisterForm(request.form)
    if request.method == 'POST':
        username = form.name.data.title()
        email = form.email.data.capitalize()
        password = generate_password_hash(form.password.data, method='sha256')        
        new_user = User(name=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    login
    """
    form = LoginForm(request.form)
    print(form.errors)
    print(form.validate())
    if request.method == 'POST' and form.validate():
        print(form)
        username = form.name.data.title()
        email = form.name.data.capitalize()
        password = form.password.data
        user = User.query.filter_by(name=username).first()
        if not user:
            user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return 'Invalid password'
        else:
            return 'user not found'
    else:
        print(form.errors)
    return render_template('login.html', form=form)


# :Todo account page=history payments, if subscribed, else


@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(name=current_user.name).first()
    user_data = {'username': user.name, 'email': user.email}
    check_account = Account.query.filter_by(user_id=user.id).first()
    history = History.query.filter_by(user_id=user.id).all()
    print(history)
    return render_template('dashboard.html', user=json.dumps(user_data),
                           subscribed=check_account.plan if check_account is not None else 'None', history=history)


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(name=current_user.name).first()
    account = Account.query.filter_by(user_id=user.id).first()
    return render_template('profile.html', account=account, user=user.name)


@app.route('/admin')
@login_required
def admin():
    approved_users = []
    pending_users = []
    pending = Account.query.filter_by(verified=False).all()
    approved = Account.query.filter_by(verified=True).all()
    for account in pending:
        pending_users.append(User.query.filter_by(id=account.user_id).first())
    for account in approved:
        approved_users.append(User.query.filter_by(id=account.user_id).first())
    return render_template('admin.html', pending_users=pending_users, pending=pending)


@app.route('/receive_ref')
def receive_ref():
    data = request.args
    user = User.query.filter_by(name=current_user.name).first()
    sub = Account(plan=data['plan'].replace('\n', ''),
                  user_id=user.id, reference=data['reference'])
            

    db.session.add(sub)
    db.session.commit()
    return jsonify({'response': 'success'})


@app.route('/approve')
def approved():
    print(request.args)
    get_account = Account.query.filter_by(reference=request.args['reference']).first()
    if get_account is None:
        return jsonify({'response': 'not found'})    

    get_account.verified = True
    get_account.sub_date = datetime.datetime.now()
    get_account.due_date = datetime.datetime.now()
    
    history = History(plan=get_account.plan, sub_date=get_account.sub_date, due_date=get_account.due_date, user_id=get_account.user_id)
    db.session.add(history)
    db.session.commit()
    return jsonify({'response': 'success'})
