# Using the MailGun Class
#
# The 'URL', 'API_KEY' and 'FROM' constants are part of Mailgun api which allows the
# the user to send emails using the MailGun class method. The API allows the user to
# send 300 emails and 10,000 emails month.
#
# To be able to use the 'send_email' method in the Mailgun class you must first register
# your details at 'www.mailgun.com'. Don't worry registration is free and no card
# details is needed.
#
# Once registration is completed and necessary verification are done you be given a
# sandbox account which allows the user to send 300 emails a day and 10,000 emails a month.
# The only downside is the sandbox account allows you to only send emails to your registered
# account which is good for development purposes.
#
# To send emails to other people's account you need to create/register a domain
#
# Log into your account using your newly created details, you will be greeted by a
# dashboard
#
# 1) click on the 'Domains' tab
# 2) Click the link inside 'Domain name'. The link should start with a sandbox<random numbers>
#
#
# You will then be a greeted with the follow pages details:
# These details are secret and should not be shown to anyone
#
# State: Active
# IP Address: IP Address
# SMTP Hostname: smtp.mailgun.org
# Default SMTP Login: postmaster@sandbox<your-random-key-should-be>.mailgun.org
# API Base URL https://api.mailgun.net/v3/<your-random-key-should-be>.mailgun.org/messages
# Default Password: <Random string for password>
# Key: key-<random string>
#
# Enter your details into the following mailgun_constant.py file
#
#
# 1) Enter your 'API BASE URL' in the URL constant below makes sure to end the URL with a
#    slash '/messages or it will not work
#
# 2) Enter your 'Key' in the API_KEY constant below
# 3) Enter your 'Default SMTP Login' in FROM constant below
# 4) Hit save and then you good to go


URL = # ADD your url
API_KEY = # Add your API key
FROM = # Add the from should start with post

