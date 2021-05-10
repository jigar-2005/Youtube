from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class Channel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Channel_name = db.Column(db.String(32767), nullable=False)
    email = db.Column(db.String(32767), unique=True, nullable=False)
    password = db.Column(db.String(32767), nullable=False)
    profile_image = db.Column(db.String(32767), nullable=False)
    cover_image = db.Column(db.String(32767), nullable=False)
    subscriber = db.Column(db.Integer, nullable=False)
    joined_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    channel_user_id = db.relationship('Video', backref='creator', lazy=True)


class Video(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(32767), nullable=False)
    video_title = db.Column(db.String(200), nullable=False)
    video_description = db.Column(db.String(500), nullable=False)
    video_category = db.Column(db.String(32767), nullable=False)
    video_thumbnail = db.Column(db.String(32767), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    views = db.Column(db.Integer, nullable=False)
    video_duration = db.Column(db.String(32767), nullable=False)
    video_user_id = db.Column(
        db.Integer, db.ForeignKey('channel.id'), nullable=False)


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'channel.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    reaction = db.Column(db.String(1), nullable=False)
    reaction_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_user_id = db.Column(
        db.Integer, db.ForeignKey('channel.id'), nullable=False)
    channel_user_id = db.Column(
        db.Integer, db.ForeignKey('channel.id'), nullable=False)
    subscriber_count = db.Column(db.Integer, nullable=False, default="0")
    subscribe_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey(
        'channel.id'), nullable=False)
    comment = db.Column(db.String(32767), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
