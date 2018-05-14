from flask import Blueprint, render_template, redirect, url_for

home_page_app = Blueprint('home_page_app', __name__)


@home_page_app.route('/home/')
@home_page_app.route('/home')
@home_page_app.route('/')
def home_page():
    """The home page for the given application"""
    return render_template('home/home.html')


