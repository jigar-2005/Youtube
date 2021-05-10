from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from . import db
from .models import Channel, Video, Reaction, Subscriber, Comment

views = Blueprint('views', __name__)


@views.route("/")
def home():
    try:
        subscriber_exists = db.session.query(Channel.id, Channel.Channel_name, Channel.profile_image, Subscriber.channel_user_id).filter(
            Subscriber.current_user_id == current_user.id, Subscriber.channel_user_id == Channel.id).all()[:5]
        videos = Video.query.order_by(Video.upload_date.desc()).all()
        profile_image = "/profile_image/"
        return render_template('youtube_homepage.html', current_channel=current_user, profile_image=profile_image, videos=videos, subscriber_exists=subscriber_exists)
    except:
        videos = Video.query.order_by(Video.upload_date.desc()).all()
        profile_image = "/profile_image/"
        return render_template('youtube_homepage.html', current_channel=current_user, profile_image=profile_image, videos=videos)


@views.route("/subscribe/user_id/<channel_id>", methods=['GET', 'POST'])
def subscribe(channel_id):
    subscriber_exists = Subscriber.query.filter(
        Subscriber.current_user_id == current_user.id, Subscriber.channel_user_id == channel_id).first()
    channel_info = Channel.query.filter(Channel.id == channel_id).first()
    if subscriber_exists:
        db.session.delete(subscriber_exists)
        db.session.commit()
        channel_info.subscriber = channel_info.subscriber-1
        db.session.commit()
        flash('you unsubscribed the channel', 'success')
    else:
        channel_info.subscriber = channel_info.subscriber+1
        db.session.commit()
        add_subscriber = Subscriber(current_user_id=current_user.id,
                                    channel_user_id=channel_id, subscriber_count=Subscriber.subscriber_count+1)
        db.session.add(add_subscriber)
        db.session.commit()
        flash("you subscribe the channel", 'success')
    return "<h1>successfull</h1>"


@views.route("/channel/<user_id>")
def channel(user_id):
    try:
        profile_image = "/profile_image/"
        video_thumbnail = "/video_thumbnail/"
        video_upload = "/video_upload/"
        channel_detail = Channel.query.filter(Channel.id == user_id).first()
        videos = Video.query.filter(Video.video_user_id == user_id)
        subscriber_exists = Subscriber.query.filter(
            Subscriber.current_user_id == current_user.id, Subscriber.channel_user_id == user_id).first()
        subscriber_channel_list = db.session.query(Channel.id, Channel.Channel_name, Channel.profile_image, Subscriber.channel_user_id).filter(
            Subscriber.current_user_id == current_user.id, Subscriber.channel_user_id == Channel.id).all()[:5]
        return render_template('youtube_channel.html', subscriber_channel_list=subscriber_channel_list, subscriber_exists=subscriber_exists, current_channel=current_user, profile_image=profile_image, channel_detail=channel_detail, videos=videos, video_thumbnail=video_thumbnail, video_upload=video_upload)
    except:
        profile_image = "/profile_image/"
        video_thumbnail = "/video_thumbnail/"
        video_upload = "/video_upload/"
        channel_detail = Channel.query.filter(Channel.id == user_id).first()
        videos = Video.query.filter(Video.video_user_id == user_id)
        return render_template('youtube_channel.html', current_channel=current_user, profile_image=profile_image, channel_detail=channel_detail, videos=videos, video_thumbnail=video_thumbnail, video_upload=video_upload)


@views.route("/single_video/<video_id>")
def single_video(video_id):
    try:
        comment_count = Comment.query.filter(
            Comment.video_id == video_id).count()
        comment_show = db.session.query(Channel.id, Channel.Channel_name, Channel.profile_image,
                                        Comment.comment_date, Comment.comment).filter(Comment.video_id == video_id).all()
        like_exists = Reaction.query.filter(
            Reaction.reaction == '1', Reaction.video_id == video_id, Reaction.user_id == current_user.id).scalar()
        dislike_exists = Reaction.query.filter(
            Reaction.reaction == '2', Reaction.video_id == video_id, Reaction.user_id == current_user.id).scalar()
        single_video = Video.query.filter(Video.id == video_id).first()
        subscriber_exists = Subscriber.query.filter(
            Subscriber.current_user_id == current_user.id, Subscriber.channel_user_id == single_video.creator.id).first()
        same_category_videos = Video.query.filter(
            Video.video_category == single_video.video_category).all()
        profile_image = "/profile_image/"
        single_video_url = "/video_upload/"
        single_video_creator_profile = "/profile_image/" + \
            single_video.creator.profile_image
        single_video.views = single_video.views+1
        db.session.commit()
        return render_template('youtube_single_video.html', comment_count=comment_count, subscriber_exists=subscriber_exists, current_channel=current_user, profile_image=profile_image, single_video=single_video, single_video_url=single_video_url, same_category_videos=same_category_videos, single_video_creator_profile=single_video_creator_profile, like_exists=like_exists, dislike_exists=dislike_exists, comment_show=comment_show)
    except:
        comment_count = Comment.query.filter(
            Comment.video_id == video_id).count()
        comment_show = db.session.query(Channel.id, Channel.Channel_name, Channel.profile_image,
                                        Comment.comment_date, Comment.comment).filter(Comment.video_id == video_id).all()
        single_video = Video.query.filter(Video.id == video_id).first()
        same_category_videos = Video.query.filter(
            Video.video_category == single_video.video_category).all()
        profile_image = "/profile_image/"
        single_video_url = "/video_upload/"
        single_video_creator_profile = "/profile_image/" + \
            single_video.creator.profile_image
        single_video.views = single_video.views+1
        db.session.commit()
        return render_template('youtube_single_video.html', comment_count=comment_count, current_channel=current_user, profile_image=profile_image, single_video=single_video, single_video_url=single_video_url, same_category_videos=same_category_videos, single_video_creator_profile=single_video_creator_profile, comment_show=comment_show)


@views.route("/search_data", methods=['GET', 'POST'])
def search_data():
    try:
        if request.method == 'POST':
            form = request.form
            search_value = form['search_data']
            search = "%{}%".format(search_value)
            videos = Video.query.filter(Video.video_title.like(
                search)).order_by(Video.upload_date.desc()).all()
            if form['search_data'] == "":
                return redirect(url_for('views.home'))
            else:
                subscriber_exists = db.session.query(Channel.id, Channel.Channel_name, Channel.profile_image, Subscriber.channel_user_id).filter(
                    Subscriber.current_user_id == current_user.id, Subscriber.channel_user_id == Channel.id).all()[:5]
                profile_image = "/profile_image/"
                return render_template('youtube_searchbar.html', search_word=form['search_data'], current_channel=current_user, profile_image=profile_image, videos=videos, subscriber_exists=subscriber_exists)
    except:
        if request.method == 'POST':
            form = request.form
            search_value = form['search_data']
            search = "%{}%".format(search_value)
            videos = Video.query.filter(Video.video_title.like(
                search)).order_by(Video.upload_date.desc()).all()
            if form['search_data'] == "":
                return redirect(url_for('views.home'))
            else:
                profile_image = "/profile_image/"
                return render_template('youtube_searchbar.html', search_word=form['search_data'], current_channel=current_user, profile_image=profile_image, videos=videos)
