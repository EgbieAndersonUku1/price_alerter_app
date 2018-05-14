from flask import Blueprint, render_template, url_for, redirect, abort

from items.form import ItemForm
from items.model.item import Item
from stores.models.store import Store
from utils.decorators import login_required
from utils.security.security import make_secure_file_name
from utils.uploader.upload import Uploader
import items.constant as item_constant

item_app = Blueprint('item_app', __name__, url_prefix='/items')


@item_app.route('/item/<store_id>/<int:page>')
@item_app.route('/item/<store_id>')
@login_required
def item_store_page(store_id, page=1):
    """item_store_page(str, int) -> returns render template for item

       Takes a store ID and returns all the items that belong to that particular store.

       :parameter
            `store_id`: A unique hex string that represents a single store.
                        When called returns all the items belong to the store
            `page`: The number of pages that belong to the store. Each page will
                    display several items belonging to the store.
    """
    items = Item.get_items_by_store_id(store_id, page)
    return render_template('items/items_page.html', items=items, store_id=store_id)


@item_app.route('/item/<item_id>/<store_id>')
@login_required
def delete_item(item_id, store_id):
    """Takes an item ID and deletes that item from the store"""
    Item.delete_item(item_id)
    return redirect(url_for('item_app.item_store_page', store_id=store_id))


@item_app.route('/<item_id>')
@login_required
def view_item(item_id):
    """view_item(str) -> return render template obj

       A permalink page that takes an item ID and displays that item on the page

       :parameter
          `item_id`: A unique hex string that represents a single item in the database
    """

    item = Item.get_item(item_id)

    if item is None:
        abort(404)
    item.load_price()
    return render_template('items/item_page.html', item_id=item_id, item=item)


@item_app.route('/<store_id>/create', methods=['GET', 'POST'])
@login_required
def create_item(store_id):
    """create_item(hex str) -> returns a create item template

       The create_item function takes a store_id and creates an
       item inside that store. Once the item has been created the
       item now belongs to the store. If the store is ever deleted
       the item is deleted too.

       :parameter
            `store_id`: The store ID belonging to the particular store
    """

    form, error, msg, item = ItemForm(), '', '', Item(store_id=store_id)
    item_id = None

    if form.validate_on_submit():

        if Store.does_item_belong_to_store(store_id, form.url.data):

            item.item_name = form.item_name.data
            item.url = form.url.data
            item.description = form.description.data

            if form.image.data:
                item.item_image = _upload_image_securely(form)
            if item.save():
                msg = item_constant.SUCCESS
                item_id = item.item_id
            else:
                error = item_constant.DUPLICATE_ITEM
        else:
            error = item_constant.ITEM_INCORRECT_STORE

    return render_template('items/new_item.html', form=form,
                           msg=msg, error=error, store_id=store_id,
                           url_prefix=item.store.url_prefix,
                           item_id=item_id
                           )


def _upload_image_securely(form):
    """_upload_image_securely(form obj) -> returns file

       Allows the user to upload an item image to the database from
       the GUI field
    """
    secure_file = make_secure_file_name(form.image.data.filename)
    folder_path = Uploader.create_upload_folder_path(secure_file)
    form.image.data.save(folder_path)
    return secure_file

