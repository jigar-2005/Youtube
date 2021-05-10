from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from moviepy.editor import VideoFileClip
from .models import Channel, Video, Reaction, Comment
from . import db
from . import db, ALLOWED_EXTENSIONS_IMAGE, ALLOWED_EXTENSIONS_VIDEO, UPLOAD_FOLDER_VIDEO, UPLOAD_FOLDER_VIDEO_THUMBNAIL
from werkzeug.utils import secure_filename
import os

upload_video = Blueprint('upload_video', __name__)


@upload_video.route("/upload_video", methods=['GET', 'POST'])
@login_required
def upload():
    profile_image = "/profile_image/"
    if request.method == 'POST':
        video_url = request.files['video_url']
        video_title = request.form.get('video_title')
        video_description = request.form.get('video_description')
        video_category = request.form.get('video_category')
        video_thumbnail = request.files['video_thumbnail']
        if video_url and '.' in video_url.filename and \
                video_url.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO:
            video_filename = secure_filename(video_url.filename)
            video_url.save(os.path.join(UPLOAD_FOLDER_VIDEO, video_filename))
            if video_thumbnail and '.' in video_thumbnail.filename and \
                    video_thumbnail.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE:
                video_thumbnail_filename = secure_filename(
                    video_thumbnail.filename)
                video_thumbnail.save(os.path.join(
                    UPLOAD_FOLDER_VIDEO_THUMBNAIL, video_thumbnail_filename))
                video_duration = VideoFileClip(
                    "C:/Users/Ram Sharma/Desktop/python/youtube/static/video_upload/"+video_filename)
                new_video = Video(video_url=video_filename, video_title=video_title, video_description=video_description, video_category=video_category,
                                  video_thumbnail=video_thumbnail_filename, views="0", video_duration=(video_duration.duration)/60, video_user_id=current_user.id)
                db.session.add(new_video)
                db.session.commit()
                flash('Video Uploaded', 'success')
                return redirect(url_for('views.home', profile_image=profile_image))
            else:
                flash("Video thumbnail is not in correct formate", 'danger')
        else:
            flash("video is not in correct formate", 'danger')
    return render_template('youtube_upload_video.html', current_channel=current_user, profile_image=profile_image)


@upload_video.route("/like<int:video_id>", methods=["GET", "POST"])
@login_required
def like(video_id):
    addlike = Reaction(video_id=video_id,
                       user_id=current_user.id, reaction="1")
    remove_like = Reaction.query.filter(
        Reaction.reaction == '1', Reaction.video_id == video_id, Reaction.user_id == current_user.id).scalar()
    dislike_into_like = Reaction.query.filter(
        Reaction.reaction == '2', Reaction.video_id == video_id, Reaction.user_id == current_user.id).scalar()
    if remove_like:
        db.session.delete(remove_like)
        db.session.commit()
        flash('You remove like', 'success')
        return redirect(url_for('views.single_video', video_id=video_id))
    elif dislike_into_like:
        dislike_into_like.reaction = "1"
        db.session.commit()
        return redirect(url_for('views.single_video', video_id=video_id))
    else:
        db.session.add(addlike)
        db.session.commit()
        flash('You liked the post', 'success')
    return redirect(url_for('views.single_video', video_id=video_id))


@upload_video.route("/dislike<int:video_id>", methods=["GET", "POST"])
@login_required
def dislike(video_id):
    add_dislike = Reaction(
        video_id=video_id, user_id=current_user.id, reaction="2")
    remove_dislike = Reaction.query.filter(
        Reaction.reaction == '2', Reaction.video_id == video_id, Reaction.user_id == current_user.id).scalar()
    like_into_dislike = Reaction.query.filter(
        Reaction.reaction == '1', Reaction.video_id == video_id, Reaction.user_id == current_user.id).scalar()
    if remove_dislike:
        db.session.delete(remove_dislike)
        db.session.commit()
        flash('You remove dislike', 'success')
        return redirect(url_for('views.single_video', video_id=video_id))
    elif like_into_dislike:
        like_into_dislike.reaction = "2"
        db.session.commit()
        return redirect(url_for('views.single_video', video_id=video_id))
    else:
        db.session.add(add_dislike)
        db.session.commit()
        flash('You disliked the post', 'success')
    return redirect(url_for('views.single_video', video_id=video_id))


@upload_video.route("/video/<int:video_id>/comment", methods=["GET", "POST"])
@login_required
def comment_post(video_id):
    if request.method == 'POST':
        comment = Comment(comment=request.form.get(
            'youtube_comment'), video_id=video_id, channel_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been post', 'success')
        return redirect(url_for('views.single_video', video_id=video_id))
    flash('comment did not passed', 'danger')
    return redirect(url_for('views.single_video', video_id=video_id))
