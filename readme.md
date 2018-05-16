
# Price Alert application

Started on 14th April 2018 completed 

Project 98 percent complete

# Technologies Used

1) Python3.6
2) MongoEngine
3) MailGun API
4) Flask
5) CSS
6) HTML

# What is price Alerter?

**Price Alerter** is an online web based application that allows users to track the prices of any
*online item*. The app allows the user to create a given store along with the price of
the item they want to track.
 
The app will then monitor the price of the item and if the prices changes the user would be alerted of the new price by email.

The site comes with three predefined stores Ebay, Amazon and Game that allows the
user create an item which the user can then add an alert to.
           
# Using Price Alerter
#

To use Price Alerter you need to use MailGun API. The MailGun API allows
user to be able to send and receive emails.


# Registering with MailGun to send emails
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

1) State: Active
2) IP Address: IP Address
3) SMTP Hostname: smtp.mailgun.org
4) Default SMTP Login: postmaster@sandbox<your-random-key-should-be>.mailgun.org
5) API Base URL https://api.mailgun.net/v3/<your-random-key-should-be>.mailgun.org/messages
6) Default Password: < Random string for password>
7) Key: key < random string>


## Entering your details in the Mailgun_constant.py file
#

Open the Mailgun_constant file. Inside there are three constants. These are 'URL', 'API_KEY' and 'FROM'

**Enter your details into the following mailgun_constant.py file constants **

1) Enter your 'API BASE URL' in the URL constant below makes sure to end the URL with a slash '/messages or it will not work
2) Enter your 'Key' in the API_KEY constant below
3) Enter your 'Default SMTP Login' in FROM constant below
4) Hit save and then you good to go


# Running Price-alerter on your computer
#

1) Open a terminal create a folder and call it whatever you want
2) Inside that folder we are going to create a virtual environment
2) Type **virtualenv --python=python3.6 venv** and hit enter. This will create your virtuale environment
2) To activate the virtual environment on Linux enter the command **source venv/bin/activate** 
2) To activate the virtual environment on Window enter the command **\venv\Scripts\activate**
2) Now the run the command **pip3.6 install -r requirement.txt**. This download all the programs needed to run the program. Make sure that your are running it inside a virtual machine this allows you to easily delete the app by deleting the virtual machine
2) Enter your administrator e-mail in src/config.py this is the email that you used to register with **the MAILGUN website**.
3) Define your Mailgun API details on src/models/alerts/constants.py
4) In the settings file for the *UPLOAD FOLDER* replace the path with the pathway to your img directory. 
   e.g /home/some pathway/static/img. This is where your images would be stored
4) change your secret key if you wish
4) Run the command **mongod** to activate the mongo server. In some case you might need to run it with admin priviledges
5) Run the Flask server by running **python run.py runserver**


# Running the application

1) Open a browser and enter the url **http://127.0.0.1:5000/register/**

![register](https://user-images.githubusercontent.com/7634091/40142666-2e25e0be-5951-11e8-83a8-aad51d6ba612.png)

2) Register your details. Unfortuntately because you are using Mailgun the free tier the email you use to register with the app must be the one you used to register with MailGun. This is where the verification email will be sent to.
3) Verify your email

4) Login to the app

![login](https://user-images.githubusercontent.com/7634091/40142786-9153485c-5951-11e8-8b21-e092006b895f.png)

5) Click on my stores

![my_stores](https://user-images.githubusercontent.com/7634091/40142966-063517a4-5952-11e8-9293-949d3cdb7080.png)

6) You will be created with a button telling you that you have not created any stores yet

![no_stores](https://user-images.githubusercontent.com/7634091/40143092-56ee4b02-5952-11e8-9c70-c45870c7c708.png)


7) Enter the details for your new store. For knowledge on how to create the span and store query see the about about page. In this example we will be creating the store ebay and all items created will belong to the ebay store

![ebay](https://user-images.githubusercontent.com/7634091/40143494-795a3c9a-5953-11e8-84ac-d9a1630dab0b.png)

8) After hitting create store you will be greeted with this page

![new_store](https://user-images.githubusercontent.com/7634091/40147014-c427213c-595f-11e8-8a40-a0e53c1ec954.png)

9) Click on view store

![view_store](https://user-images.githubusercontent.com/7634091/40143882-989c4b2e-5954-11e8-8542-4f164a2b9508.png)

10) Click on create item. 

![new_item](https://user-images.githubusercontent.com/7634091/40144091-4ae1bd3c-5955-11e8-816d-ff16294e0e37.png)

11) Click on the create button

![success](https://user-images.githubusercontent.com/7634091/40144270-f53a3f8e-5955-11e8-9d02-3a9d4316e5e7.png)

Note the item url must be a prefix of the store. For example if the store prefix is https://www.ebay.com then item url must be
https://www.ebay.com/some-random-string. If the item Url prefix does not match the store's url then error will be thrown. If the item already exists then an error message will also be thrown

### If the item's url does not match the store's prefix an error would also be thrown

![does_not_match](https://user-images.githubusercontent.com/7634091/40144681-5abe7202-5957-11e8-9d81-bcf42681e829.png)

### Adding an item to the db that will result in an error if the item already exists

![item_already_exists](https://user-images.githubusercontent.com/7634091/40144470-ae4081a0-5956-11e8-88ed-1f2c9a2d9f34.png)


12) To view an item
  *Click on my store
  *Go to store you wish to view the item and click
  *Inside you will see all items belong to the store
  *Click on view item
  
  ![view_item](https://user-images.githubusercontent.com/7634091/40144949-0a3a8a4a-5958-11e8-9c0f-c44f406191c3.png)
  
  ![blue_ray_player](https://user-images.githubusercontent.com/7634091/40145823-3d018124-595b-11e8-80da-b0fc651b16b5.png)

  ![blue_ray_player_2](https://user-images.githubusercontent.com/7634091/40145841-4732e1c4-595b-11e8-8cb6-c29d5843afdf.png)

#### Notice the item has no alert in the image number 12
#### To add an alert to an item hit the alert button. This enables an alert to be set to an item. You will then be notified by email whenever your item's prices reaches that limit.

### Let add £40 to our alert. We shall now be alerted should our item price hit £40

![new_alert](https://user-images.githubusercontent.com/7634091/40147204-b2ae66bc-5960-11e8-8edf-c9ee28cae82c.png)

### Now if click active alerts page we see

![active_alert](https://user-images.githubusercontent.com/7634091/40147389-5969fab6-5961-11e8-84fb-2ba188e5d299.png)

### Notice that our alerts message at the top of the page is now active

![active_alert_image](https://user-images.githubusercontent.com/7634091/40146051-0c162d20-595c-11e8-9a75-690d6dc79184.png)

### We can also disable 

![disabled_alert](https://user-images.githubusercontent.com/7634091/40146650-441dd090-595e-11e8-98ec-77e4d853e1a2.png)


### or delete the alert
![delete_alerted](https://user-images.githubusercontent.com/7634091/40146759-a814e70a-595e-11e8-98f9-71a6a6d3fec1.png)
  



Continue rest of the readme file tommorrow
    

