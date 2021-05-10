from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Channel
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)


@auth.route('/sign-in', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    elif request.method == 'POST':
        channel = Channel.query.filter_by(
            email=request.form.get('email')).first()
        if channel and check_password_hash(channel.password, request.form.get('password')):
            login_user(channel, remember=True)
            db.session.commit()
            return redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("youtube_login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        Channel_name = request.form.get('Channel_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        profile_image = request.form.get('profile_image')
        cover_image = request.form.get('cover_image')
        subscriber = request.form.get('subscriber')
        channel_email_exit = Channel.query.filter_by(email=email).first()
        channel_name_exit = Channel.query.filter_by(
            Channel_name=Channel_name).first()
        if channel_email_exit:
            flash('Email already exists.', 'danger')
            return render_template("youtube_register.html")
        elif channel_name_exit:
            flash('Channel name already exists.', 'danger')
            return render_template("youtube_register.html")
        elif password != confirm_password:
            flash('Passwords don\'t match.', 'danger')
            return render_template("youtube_register.html")
        else:
            new_channel = Channel(Channel_name=Channel_name, email=email, password=generate_password_hash(
                password, method='sha256'), subscriber="0", profile_image="user_profile_img.jpg", cover_image="default_cover_image.png")
            db.session.add(new_channel)
            db.session.commit()
            flash('Account created!, You are now able to log in', 'success')
            return render_template("youtube_login.html")
    return render_template("youtube_register.html")
