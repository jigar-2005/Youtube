from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from .models import Channel, Video, Reaction, Comment
from . import db
from . import db, ALLOWED_EXTENSIONS_IMAGE, UPLOAD_FOLDER_PROFILE_IMAGE, UPLOAD_FOLDER_COVER_IMAGE
from werkzeug.utils import secure_filename
import os

setting = Blueprint('setting', __name__)


@setting.route("/manage_profile", methods=['GET', 'POST'])
@login_required
def manage_profile():
    profile_image = "/profile_image/"
    if request.method == 'POST':
        if request.form.get('profile_image_new') != "":
            profile_image_data = request.files['profile_image_new']
            if profile_image_data and '.' in profile_image_data.filename and \
                    profile_image_data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE:
                current_user_profile_image = secure_filename(
                    profile_image_data.filename)
                profile_image_data.save(os.path.join(
                    UPLOAD_FOLDER_PROFILE_IMAGE, current_user_profile_image))
                current_user.profile_image = current_user_profile_image
                db.session.commit()
        else:
            current_user.profile_image = current_user.profile_image
            db.session.commit()
        if request.form.get('cover_image_new') != "":
            cover_image_data = request.files['cover_image_new']
            if cover_image_data and '.' in cover_image_data.filename and \
                    cover_image_data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE:
                current_user_cover_image = secure_filename(
                    cover_image_data.filename)
                cover_image_data.save(os.path.join(
                    UPLOAD_FOLDER_COVER_IMAGE, current_user_cover_image))
                current_user.cover_image = current_user_cover_image
                db.session.commit()
        else:
            current_user.cover_image = current_user.cover_image
            db.session.commit()
        current_user.Channel_name = request.form.get('Channel_name_new')
        current_user.email = request.form.get('email_new')
        db.session.commit()
        flash("account update", 'success')
    return render_template('youtube_manage_profile.html', current_channel=current_user, profile_image=profile_image)
