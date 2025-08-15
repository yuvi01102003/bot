from flask import Flask, Blueprint, render_template, request, flash, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from bot import db
from flask_login import login_required, logout_user, login_user, current_user
from bot.utils import generate_otp, send_otp_email

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        passowrd = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        user = Users.query.filter_by(email=email).first()

        if user:
            flash('Email already Exists', category='error')
        elif len(name) < 2:
            flash("Name is too short..!", category='error')
        elif not '@' in email:
            flash("Check the Email address..! incorrect!", category='error')
        elif len(phone) < 10:
            flash("Check the Phone Number..! ", category='error')
        elif len(passowrd) < 5:
            flash('Password is Small..!', category='error')
        elif passowrd != confirmpassword:
            flash('Both Password does not match', category='error')
        else:
            otp_code = generate_otp() 
            hashed_password = generate_password_hash(passowrd, method='pbkdf2:sha256', salt_length=16)
            new_user = Users(name=name, email=email, phone=phone, password=hashed_password, otp=otp_code, is_verified=False)
            db.session.add(new_user)
            db.session.commit()
            send_otp_email(email, otp_code)
            flash('check OTP in your email', category='success')
            return redirect(url_for('auth.verify_otp', email=email))
    return render_template('signup.html', user=current_user)


@auth.route('/verify_otp/<email>', methods=['GET', 'POST'])
def verify_otp(email):
    user = Users.query.filter_by(email=email).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if user.otp == entered_otp:
            user.is_verified = True
            user.otp = None
            db.session.commit()
            flash('Email verified successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid OTP, please try again.', 'error')

    return render_template('verify_otp.html', email=email, user=current_user)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password) and user.is_verified == True:
                flash('Logging in Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.indexPage'))
            else:
                flash('Password not matched..!', category='error')
        else:
            flash('Email does not Exist', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Loggin out Successfully', category='success')
    return redirect(url_for('auth.login'))