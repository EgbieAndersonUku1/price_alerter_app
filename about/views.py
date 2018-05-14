from flask import render_template, Blueprint

from stores.models.store import Store

about_app = Blueprint('about_app', __name__, url_prefix="/about")


@about_app.route('/<page>')
@about_app.route('/')
def about_page(page=1):
    """"""
    stores = Store.get_store_fields(page)
    return render_template('about/about_page.html', stores=stores)



