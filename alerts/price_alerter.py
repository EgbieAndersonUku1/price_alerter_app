from alerts.models import Alert


# This sends a price alert email to the user email whenever an item matches the user
# alert price

items_to_update = Alert.get_items_to_update()


for alert in items_to_update:

    alert.load_price()
    alert.send_email_to_user_if_item_matches_price_limit()
