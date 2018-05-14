from flask import Blueprint, render_template, request, url_for, redirect

from alerts.models.alert import Alert
from alerts.form import NewAlertForm, EditAlertForm
from items.model.item import Item
from utils.decorators import login_required
from utils.security.security import is_safe_url

alert_app = Blueprint('alert_app', __name__, url_prefix='/alerts')


@alert_app.route('/alerts')
@alert_app.route('/all/<int:page>')
@login_required
def all_alerts(page=1):
    """Returns all alerts set by the user"""
    return render_template('alerts/alerts.html', alerts=Alert.get_alerts(page))


@alert_app.route('/new/alert/<item_id>', methods=['GET', 'POST'])
@login_required
def create_alert(item_id):
    """create_alert(string id) -> returns redirect or render form object

       Takes an item id and creates a new alert for that item

       :parameter
          `item_id`: An item ID that allow the user to create an alert for that item
    """

    item = Item.get_item_by_id(item_id=item_id)
    form = NewAlertForm()

    if item and form.validate_on_submit():
        alert = Alert(price_limit=form.alert_limit.data,
                      item_id=item_id,
                      )

        item.alert_added = True
        item.alert = alert.save()
        item.save()

        return redirect(url_for('alert_app.all_alerts', page=1))

    return render_template('alerts/new_alert.html', form=form, item_id=item_id, item=item)


@alert_app.route('/edit/<alert_id>', methods=['GET', 'POST'])
@login_required
def edit_my_alert(alert_id):
    """edit_my_alert(string id) -> returns render template or redirect obj

       Allows the user to edit an active alert.

       :parameter
          `alert_id`: An string ID that represents a given alert
    """

    alert, error = Alert.get_alert_by_id(alert_id), ''
    form = EditAlertForm()

    if request.method == 'POST' and form.validate_on_submit():

        alert.update({'price_limit': form.alert_limit.data})
        return redirect(url_for('user_app.user_alerts'))

    try:
        return render_template('alerts/edit_alert.html', form=form, alert=alert, alert_id=alert_id, error=error)
    except:
        return redirect(url_for('.alert_creation_error'))


@alert_app.route('/deactivate/<item_id>/<alert_id>')
@login_required
def deactivate_alert(item_id, alert_id):
    """deactivate_alert(string ID, string ID) -> returns redirect obj

       Allows the user to deactivate an alert for a given item. Note
       the alert must be created and active

       :parameter
            `item_id` : A string ID that represents a given item
            `alert_id`: A String ID that represents an alert for a given item
    """
    Alert.deactivate_alert(item_id, alert_id)

    if is_safe_url(request.referrer):
       return redirect(request.referrer)
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_app.route('/activate/<item_id>/<alert_id>')
@login_required
def activate_alert(item_id, alert_id):
    """activate_alert(string ID, string ID) -> returns redirect obj

       Allows the user to activate an alert for a given item. Note
       the item must already have alert and it must be disabled.

       :parameter
          `item_id` : A string ID that represents a given item
          `alert_id`: A String ID that represents an alert for a given item
    """

    Alert.activate_alert(item_id, alert_id)

    if is_safe_url(request.referrer):
        return redirect(request.referrer)
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_app.route('/delete/alert/<item_id>/<alert_id>')
@login_required
def delete_alert(item_id, alert_id):
    """delete_alert(string ID, string ID) -> returns redirect obj

       Allows the user to delete an alert for a given item. Note
       the item must already have alert.

       :parameter
            `item_id` : A string ID that represents a given item
            `alert_id`: A String ID that represents an alert for a given item
    """

    Alert.delete_alert_by_id(item_id, alert_id)
    return redirect(url_for('.all_alerts', page=1))


@alert_app.route('/my_alert/<alert_id>')
@alert_app.route('/my_alert')
@login_required
def get_alert_page(alert_id=None):
    """get_alert_page(str ID default None) -> returns redirect obj or render template

       A permalink page that returns an alert for a given item

       :parameter
            `alert_id`: The alert ID for a given item
    """

    alert = Alert.get_alert_by_id(alert_id)
    if not alert:
        return redirect(url_for('.alert_not_created_error'))
    return render_template('alerts/alert.html', alert=Alert.get_alert_by_id(alert_id))


@alert_app.route('/check/price/<alert_id>')
@login_required
def check_price_for_alert(alert_id):
    """check_price_for_alert(string ID) -> returns (redirect obj or render template)

       Checks whether the user's item has reached the given price that was set by
       the user

       :parameter
            `alert_id`: The alert ID for a given item
    """

    try:
        alert = Alert.load_alert(alert_id)
    except ValueError:
        return redirect(url_for('.check_price_error'))
    else:
        alert.load_price(fetch_new=True)
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_app.route('/price/error')
@login_required
def alert_not_created_error():
    """Returns an error page if the user has not created an alert"""
    return render_template('alerts/alert_error.html')

