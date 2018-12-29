# Project: Catalog App

The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, 
as well as provide a user registration and authentication system.

### About
The user-facing newspaper site frontend itself, and the database behind it
This project provides a simple Logs Analysis internal reporting tool.
Reporting tool use to Retrieving Data from postgresql.

### Tools used
1.Vagrant
2.VirtualBox
3.Git Bash terminal 


### How to run

We're using tools called Vagrant and VirtualBox to install and manage the VM.
 1. If vagrant is successfully installed ,you will able to run vagrant --version
 2.To start the VM run the vagrant up
 3.When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM
 4.The PostgreSQL database server will automatically be started inside the VM. You can use the psql command-line tool to access it and run SQL statements:
 5. Logging out and in
 If you type exit (or Ctrl-D) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type vagrant ssh again.
 If you reboot your computer, you will need to run vagrant up to restart the VM.





### Run the DB Script
name :database_setup.py (for reating DB and Table)
>>python database_setup.py
(then the same path DB file will reate name "sportscatalog" )
For meata data 
>>python sportscatalog_metadata.py


### Tables
1.user
2.catalog
3.catalog_Item

### To run the script `application.py`. 

Setp : python application.py
then hit the URL :http://localhost:8000/

###  User Type
1.General User(They can vist the catalof app but they can't Add/Edit/Delete the Catalog Item)
2.Google User (They can vist the catalof and  but the can Add new Catalog item but they can't Edit/Delete the Catalog Item created by other user)
3.Facebook User  (They can vist the catalof and  but the can Add new Catalog item but they can't Edit/Delete the Catalog Item created by other user)

###  2.Google User(Google OAuth2) Configuration Steps

Google has changed the user interface for obtaining OAuth credentials since this video was created. The functionality is the same, but the appearance is somewhat different from what's depicted here.

1.Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
2.Choose Credentials from the menu on the left.
3.Create an OAuth Client ID.
4.This will require you to configure the consent screen.
5.When you're presented with a list of application types, choose Web application.
6.You can then set the authorized JavaScript origins, with the same settings as in the video.
7.You will then be able to get the client ID and client secret.
You can also download the client secret as a JSON data file once you have created it.

IMPORTANT: Depending on the version of Flask you have, you may or may not be able to store a credentials object in the login_session the same way that Lorenzo does. You may get the following error:

OAuth2Credentials object is not JSON serializable

What should you do to fix this? There are three options:

Rather than storing the entire credentials object you can store just the access token instead. It can be accessed using credentials.access_token.
The OAuth2Credentials class comes with methods that can help you. The .to_json() and .from_json() methods can help you store and retrieve the credentials object in json format.
Update your versions of Flask, _ and _ to match Lorenzo's. Use the following commands:
pip install werkzeug==0.8.3
pip install flask==0.9
pip install Flask-Login==0.1.3

Note: If you get a permissions error, you will need to include sudo at the beginning of each command. That should look like this: sudo pip install flask==0.9

Go to the GoogleDevConsole> API & Auth> Credentials>Select your app> Authorized Redirect URIs and add the following URIS: http://localhost:8000/login and http://localhost:8000/gconnect You may have to change the port number depending on the port number you have set your app to run on.



###  3.Facebook User Configuration Steps

Facebook Configure URL : https://developers.facebook.com/
Facebook Configuration file URL : https://github.com/udacity/ud330/blob/master/Lesson4/step2/fb_client_secrets.json
Facebook has changed recently and only allows to use HTTPS protocol for redirect urls, please follow the following steps to be able to use localhost:

1.Create an Application.
2.Configure the URL site as: http://localhost:8000/
3.Create a Test Application from the button in the apps dropdown.
4.Don't change the default values.
5.Use in your application code the Test Application Application Id and Secret phrase
 


