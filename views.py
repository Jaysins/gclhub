# coding=utf-8
"""
Views.py
"""


from flask import render_template, request, url_for, json, jsonify, redirect, g
from functools import wraps
# noinspection PyUnresolvedReferences
from models import User, History, Account
# noinspection PyUnresolvedReferences
from app import app, db, login_manager, s, mail
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, login_user, current_user
from itsdangerous import SignatureExpired
# noinspection PyUnresolvedReferences
from forms import RegisterForm, LoginForm, AdminLoginForm, AddNewForm
from flask_mail import Message
from calendar import monthrange


# :Todo implement forgot password
# :Todo implement edit page
# :Todo confirm email


def change_date():
    date = datetime.datetime.now()

    c = monthrange(date.year, date.month)

    date_check = [date.year, date.month, date.day]

    if c[1] == date.day:
        print('end of the month')
        date_check[1] += 1
        date_check[2] = 2
    else:
        date_check[2] += 1

    date_to = datetime.date(date_check[0], date_check[1], date_check[2])
    return date_to


def add_one_month(t):
    one_day = datetime.timedelta(days=1)
    one_month_later = t + one_day
    print(one_month_later.month)
    print(t.month)
    while one_month_later.month == t.month:  # advance to start of next month
        one_month_later += one_day
    target_month = one_month_later.month
    while one_month_later.day < t.day:  # advance to appropriate day
        one_month_later += one_day
        if one_month_later.month != target_month:  # gone too far
            one_month_later -= one_day
            break
    return one_month_later


def admin_login_required(f):
    """

    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        g.user = current_user
        print(g.user)
        print(g.user.is_admin)
        print(g.user.is_admin)
        try:
            if g.user is None or g.user.is_admin is False or g.user.is_admin is None:
                return redirect(url_for('admin_login', next=request.url))
        except AttributeError:
            return redirect(url_for('admin_login', next=request.url))

        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    """

    :param user_id:
    :return:
    """
    # noinspection PyUnresolvedReferences
    return User.query.get(int(user_id))


def confirm(email, user_id, username, ref):
    """

    :return:
    """
    token = s.dumps(email, salt='email-confirm')    
    link = url_for('confirm_email', token=token, _external=True, user_id=user_id) if ref != 'approve' else url_for('login', _external=True)
    print(ref)
    if ref == 'signup':        
        body = f'Dear {username}, welcome please Click to verify your account {link}'
        header = 'Email Confirmation'
    elif ref == 'receive':
        body = f'Dear {username}, Your account activation is pending, you will be notified soon as payment is verified'
        header = 'Acoount Pending'
    elif ref == 'approve':
        body = f'Dear {username}, Your payment has been successfully approved and your account verified,<br> your account is now active as of today{datetime.datetime.now()}, please click {link}'
        header = 'Account Approved'
    else:
        body = f'Dear {username}, please Click to verify your email address {link}.'
    # msg = Message(f'{header}', sender='jaysinscars@gmail.com', recipients=[email])
    # msg.body = body
    # mail.send(msg)
    print(body)
    print(link)


@app.route('/')
def index():
    """
    index
    """
    try:
        print(current_user.name)
        return redirect(url_for('dashboard'))
    except AttributeError:    
        return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup
    """
    try:
        print(current_user.name)
        return redirect(url_for('dashboard'))
    except AttributeError:            
        error = ''
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.name.data.title()
            email = form.email.data.capitalize()
            check_valid = User.query.filter_by(name=username).first()
            if check_valid is None:
                check_valid = User.query.filter_by(email=email).first()
            if check_valid is not None:                
                return render_template('signup.html', error='Username or Email already taken', user='user', form=form)
            password = generate_password_hash(form.password.data, method='sha256')      

            new_user = User(name=username, email=email, password=password, is_admin=False, verified=False)
            db.session.add(new_user)
            db.session.commit()
            confirm(email, new_user.id, new_user.name, ref='signup')
            
            return redirect(url_for('confirm_message', user_id=new_user.id))
        else:
            get_error = ''
            print(form.errors)
            if form.errors:
                for errors in form.errors:
                    get_error = errors
                    break
                error = 'please enter a valid {}'.format(get_error) if 'Match' not in form.errors[get_error][0] else form.errors[get_error][0]
        return render_template('signup.html', form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    login
    """
    try:
        print(current_user.name)
        return redirect(url_for('dashboard'))
    except AttributeError:
        message = ''        
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.name.data.title()
            email = form.name.data.capitalize()
            password = form.password.data
            user = User.query.filter_by(name=username).first()
            if not user:
                user = User.query.filter_by(email=email).first()
            if user:
                if user.verified is True:
                    if check_password_hash(user.password, password):
                        login_user(user)
                        if user.is_admin is True:
                            return redirect(url_for('admin'))
                        return redirect(url_for('dashboard'))
                    else:
                        return render_template('login.html', form=form, error='Invalid Password')
                else:
                    return redirect(url_for('confirm_message', user_id=user.id))
            else:
                return render_template('login.html', form=form, error='Invalid Email or Username')
        else:            
            print(form.errors)
            get_error = ''
            if form.errors:
                for errors in form.errors:
                    get_error = errors
                    break
                message = 'please enter a valid {}'.format(get_error)
        return render_template('login.html', form=form, error=message)


@app.route('/confirm_message/<int:user_id>')
def confirm_message(user_id):
    """

    :return:
    """
    user = User.query.filter_by(id=user_id).first()
    if user:
        return render_template('confirm.html', user_email=user.email, userId=user_id)
    else:
        # return redirect(url_for('error', message=''))
        return 'error not found'


@app.route('/confirm_email/<token>/<user_id>')
def confirm_email(token, user_id):
    """

    :param token:
    :param user_id:
    :return:
    """
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        get_user = User.query.filter_by(id=user_id, email=email).first()
        if get_user:
            get_user.verified = True
            db.session.commit()
            return redirect(url_for('login'))
        # :Todo return redirect(url_for('error', message='User not found'))
        return 'User not found'
    except SignatureExpired:
        return redirect(url_for('error', message='This link is expired'))


@app.route('/refresh')
def refresh():
    """

    :return:
    """
    try:
        user = User.query.filter_by(email=request.args['email']).first()
        if user.verified is True:
            return redirect(url_for('login'))
        confirm(request.args['email'], user.id, user.name, ref='signup')
        return jsonify({'status': 'success'})
    except AttributeError:
        # :Todo return redirect(url_for('error', message=''))
        return 'error refresh'


# :Todo account page=history payments, if subscribed, else
@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(name=current_user.name).first()
    user_data = {'username': user.name, 'email': user.email}
    check_account = Account.query.filter_by(user_id=user.id).first()
    print(user.id)
    history = History.query.filter_by(user_id=user.id).order(History.id.desc()).all()    
    print(history)
    return render_template('dashboard.html', user=json.dumps(user_data),
                           subscribed=check_account.plan if check_account is not None else 'None', history=history)


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(name=current_user.name).first()
    account = Account.query.filter_by(user_id=user.id).first()
    return render_template('profile.html', account=account, user=user.name)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm(request.form)
    if request.method == 'POST':        
        if form.validate():
            username = form.name.data.title()
            password = form.password.data
            user = User.query.filter_by(name=username).first()
            if current_user.name == username:
                if password == 'adminuser':
                    if user.is_admin is False or user.is_admin is None:
                        user.is_admin = True
                        db.session.commit()
                    login_user(user)
                    return redirect(url_for('admin'))
                else:
                    # TODO: ERROR MESSAGE
                    return 'admin password fail'
                # TODO: ERROR MESSAGE
            return 'please logout and try again'
        else:
            return 'invalid data, please retry'
    name = current_user.name
    return render_template('adminLogin.html', form=form, name=name)


@app.route('/admin')
@login_required
@admin_login_required
def admin():
    approved_users = []
    approved = Account.query.filter_by(verified=True).order_by(Account.id.desc()).all()
    for account in approved:
        approved_users.append(User.query.filter_by(id=account.user_id).first())
    return render_template('admin.html', approved_users=approved_users, approved=approved)


@app.route('/admin/add_new', methods=['GET', 'POST'])
@login_required
@admin_login_required
def add_new():
    form = AddNewForm(request.form)
    if request.method == 'POST' and form.validate():
        print(request.form['time'])
        date =  datetime.datetime.strptime(str(form.date.data), "%Y-%m-%d")
        time = request.form['time']
        if len(time) == 4:
            hour = int(time[0])
            minute = int(time[2] + time[3])
        elif len(time) == 5:
            hour = int(time[0] + time[1])
            minute = int(time[3] + time[4])
        else:
            return
        date = date.replace(minute=minute, hour=hour, second=00)        
        due_date = date + datetime.timedelta(hours=int(form.hours.data))
        manual_user = User(name=form.name.data.title(), email=form.email.data.capitalize())        
        db.session.add(manual_user)
        db.session.commit()        
        manual_account = Account(plan=form.space.data.title(), user_id=manual_user.id, sub_date=date, due_date=due_date, verified=True, manual=True)
        db.session.add(manual_account)
        db.session.commit()        
    else:
        print(form.errors)
    return render_template('add_new.html', form=form)


@app.route('/admin/new_requests')
@login_required
@admin_login_required
def new_requests():
    pending_users = []
    pending = Account.query.filter_by(verified=False).order_by(Account.id.desc()).all()
    for account in pending:
        pending_users.append(User.query.filter_by(id=account.user_id).first())
    return render_template('new_requests.html', pending_users=pending_users, pending=pending)


@app.route('/receive_ref')
def receive_ref():
    data = request.args
    user = User.query.filter_by(name=current_user.name).first()
    sub = Account(plan=data['plan'].replace('\n', ''),
                  user_id=user.id, reference=data['reference'])
            

    db.session.add(sub)
    db.session.commit()

    confirm(user.email, user.id, user.name, ref='receive')
    return jsonify({'response': 'success'})


@app.route('/approve')
def approved():
    print(request.args)
    get_account = Account.query.filter_by(reference=request.args['reference']).first()

    if get_account is None:
        return jsonify({'response': 'not found'})    
    user = User.query.filter_by(id=get_account.user_id).first()
    get_date = change_date()
    due_date = add_one_month(get_date)

    get_account.verified = True
    get_account.sub_date = datetime.datetime.now()
    get_account.due_date = due_date
    history = History(plan=get_account.plan, sub_date=get_account.sub_date, due_date=get_account.due_date, user_id=get_account.user_id)    
    db.session.add(history)
    db.session.commit()    
    ref = 'approve'
    confirm(user.email, user.id, user.name, ref)
    return jsonify({'response': 'success'})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))