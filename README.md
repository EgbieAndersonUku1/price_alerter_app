

Price Alert application
Project complete
Started on 14th April 2018 completed on 14th May 2018.

Technologies Used

Python3.6

MongoEngine

MailGun API

Flask

CSS

HTML

What is price Alerter?

**Price Alerter** is an online web based application that allows users to track the prices of any
*online item*. The app allows the user to create a given store along with the price of
the item they want to track.
 
The app will then monitor the price of
the item and if the prices changes the user would be alerted of the new price by email.

The site comes with three predefined stores Ebay, Amazon and Game that allows the
user create an item which the user can then add an alert to.
            
            
        
#Using Price Alerter
#

To use Price Alerter you need to use MailGun API. The MailGun API allows
user to be able to send and receive emails.


###Registering with MailGun to send emails
#

To be able to use the *send_email* method in the Mailgun class file you must first register
your details at *www.mailgun.com*. Don't worry registration is free and no card
details is needed.

Once registration is completed and necessary verification are done you be given a
sandbox account which allows the user to send 300 emails a day and 10,000 emails a month.
The only downside is the sandbox account allows you to only send emails to your registered
account which is good for development purposes.


To send emails to other people's account you need to create/register a domain

Log into your account using your newly created details, you will be greeted by a dashboard

1) click on the 'Domains' tab
2) Click the link inside 'Domain name'. The link should start with a sandbox<random numbers>


You will then be a greeted with the follow pages details:
These details are secret and should not be shown to anyone

State: Active
IP Address: IP Address
SMTP Hostname: smtp.mailgun.org
Default SMTP Login: postmaster@sandbox<your-random-key-should-be>.mailgun.org
API Base URL https://api.mailgun.net/v3/<your-random-key-should-be>.mailgun.org/messages
Default Password: < Random string for password>
Key: key < random string>



#Entering your details in the Mailgun_constant.py file
#


The 'URL', 'API_KEY' and 'FROM' constants are part of Mailgun api which allows the
the user to send emails using the MailGun class method. The API allows the user to
send 300 emails and 10,000 emails month.

Enter your details into the following mailgun_constant.py file

1) Enter your 'API BASE URL' in the URL constant below makes sure to end the URL with a slash '/messages or it will not work

2) Enter your 'Key' in the API_KEY constant below
3) Enter your 'Default SMTP Login' in FROM constant below
4) Hit save and then you good to go



#Running Price-alerter on your computer
#

1) Clone the repository
2) Open a terminal and type the command git clone 
2) Enter your administrator e-mail in src/config.py.
3) Define your Mailgun API details on src/models/alerts/constants.py
4) In the settings file for the *UPLOAD FOLDER* replace the path with the pathway to your img directory. 
   e.g /home/some pathway/static/img. This is where your images would be stored
4) change your secret key
4) Create a virtual environment for the repository (run virtualenv --python=python3.5 venv)
5) Run the Flask server by running python run.py runserver
5) Make sure that your are running it inside a virtual machine this allows you to easily delete the app by deleting the virtual machine
    

