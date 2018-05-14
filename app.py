from flask_mongoengine import MongoEngine
from flask import Flask, render_template
from flask_cache import Cache

app = Flask(__name__)


cache = Cache(config={
    'CACHE_TYPE': 'memcached',
    'CACHE_MEMCACHED_SERVERS': ['127.0.0.1:11211'],
    'CACHE_DEFAULT_TIMEOUT': 0
})

db = MongoEngine()



@app.route('/index')
def index():
    return render_template('index.html')


def create_app(**config_overrides):
    """"""

    from registration.views import registration_app
    from login.views import login_app
    from password.views import password_app
    from home_page.views import home_page_app
    from stores.views import stores_app
    from alerts.views import alert_app
    from items.views import item_app
    from about.views import about_app
    from logout.views import logout_app

    app.config.from_pyfile('settings.py')
    app.config.from_object('config')
    app.config.update(config_overrides)

    db.init_app(app)
    cache.init_app(app)

    # when clearing the entire cache uncomment these two lines and then run the application. Once
    # this done comment the lines again
    with app.app_context():
       cache.clear()

    app.register_blueprint(registration_app)
    app.register_blueprint(login_app)
    app.register_blueprint(password_app)
    app.register_blueprint(home_page_app)
    app.register_blueprint(stores_app)
    app.register_blueprint(alert_app)
    app.register_blueprint(item_app)
    app.register_blueprint(about_app)
    app.register_blueprint(logout_app)

    return app