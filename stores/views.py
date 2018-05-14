import json
from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

import stores.constants as store_constants
from stores.form import NewStoreForm, EditStoreForm
from stores.models.store import Store
from utils.decorators import login_required


stores_app = Blueprint('stores_app', __name__, url_prefix='/stores')


@stores_app.route('/store_name/<store_name>')
@login_required
def get_store_by_name(store_name):
    """"""
    return redirect(url_for('stores_app.store_page', store_id=Store.get_store_id_by_name(store_name)))


@stores_app.route('/')
@stores_app.route('/<page>')
@login_required
def available_stores(page=1):
    stores = Store.get_all_stores(page)
    return render_template('stores/stores.html', stores=stores)


@stores_app.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_page(store_id):
    """"""
    return render_template('stores/store.html', store=Store.get_store_by_id(store_id))


@stores_app.route('/create', methods=['GET', 'POST'])
@login_required
def create_store():

    form, error = NewStoreForm(), ''
    edit_store = False

    if form.validate_on_submit():

        try:

            Store(store_name=form.store_name.data,
                  description=form.description.data,
                  url_prefix=form.url_prefix.data,
                  tag_name=form.tag_name.data,
                  query=json.loads(form.query.data),
                  ).save()

            return redirect(url_for('.available_stores'))

        except json.JSONDecodeError:
            error = store_constants.JSON_ERROR
        except:
            error = store_constants.STORE_EXISTS_ERROR

    return render_template('stores/new_store.html', form=form, error=error, edit_store=edit_store)


@stores_app.route('/edit/<store_id>', methods=['GET', 'POST'])
@login_required
def edit_store(store_id):
    """"""

    store, edit_store = Store.get_store_by_id(store_id), True
    form = EditStoreForm(obj=store)

    if form.validate_on_submit():
        store.description = form.description.data
        store.save()
        return redirect(url_for('.available_stores'))
    return render_template('stores/edit_store.html', form=form, store_id=store_id, edit_store=edit_store, store=store)


@stores_app.route('/all')
@stores_app.route('/all/<page>')
@login_required
def get_all_predefined_stores(page=1):
    """"""
    return render_template('stores/predefined_stores.html', stores=Store.get_all_predefined_stores(page))


@stores_app.route('/delete/<store_id>', methods=['GET', 'POST'])
@login_required
def delete_store(store_id):
    Store.delete_store(store_id)
    return redirect(url_for('.available_stores'))


@stores_app.route("/our-stores")
def about_stores(page=1):
    """"""
    stores = Store.get_store_fields(page)
    return render_template('about/about_page.html', stores=stores)


@stores_app.route('/creating_stores')
def creating_stores(page=1):
    """"""
    stores = Store.get_store_fields(page)
    return render_template('about/creating_stores.html', stores=stores)
