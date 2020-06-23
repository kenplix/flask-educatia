# Summary
Education platform for students and tutors written on Flask. 

This also demonstrates practical uses of several Flask modules such as:
* Flask-Admin
* Flask-Bcrypt
* Flask-Login
* Flask-Mail
* Flask-Migrate
* Flask-Script
* Flask-SQLAlchemy
* Flask-WTF

# Implementation Notes
The application follows the guidelines from [Flask Patterns for Large Applications](http://flask.pocoo.org/docs/patterns/packages/) using blueprints and decorators. It uses HTML5 Boilerplate and Bootstrap for the basic layout and design.

The project is structured as follows, following a modular-based approach:  
```
tree -d
.
├── app
│   ├── blueprints
│   │   ├── auth
│   │   ├── main
│   │   ├── posts
│   │   └── users
│   ├── static
│   │   ├── css
│   │   ├── images
│   │   │   └── profile_pics
│   │   └── js
│   └── templates
│       ├── auth
│       ├── errors
│       ├── main
│       ├── posts
│       └── users
├── logs
└─── migrations
     └── versions
```
# Running the Application
1. Clone this repository.  
```git clone https://github.com/AleksandrTolstoy/flask-educatia.git```  
2. Create virtual environment in repository.  
```
cd flask-educatia
python3 -m venv venv
```  
3. Activate virtual environment.  
```source venv/bin/activate```  
4. Install requirements.  
```python3 -m pip install -r requirements.txt```  
5. Set up the configuration data in ```.env``` file as shown below:   
```
SECRET_KEY=<Your first secret string>
CSRF_SESSION_KEY=<Your second secret string>

DATABASE_URI=<dialect+driver://username:password@host:port/database>

MAIL_SERVER=<Mail server>
MAIL_PORT=<Mail port>
MAIL_USE_TLS=<True or False>
MAIL_USERNAME=<The part before the @ symbol (local part)>
MAIL_PASSWORD=<Password for $MAIL_USERNAME@$MAIL_SERVER>

ADMIN_EMAIL=no-reply@gmail.com
ADMIN_PASSWORD=<Password for no-reply@gmail.com>
```  
SECRET_KEY is used for cryptographically signing cookies, which in turn are used for sessions. This means that cookies cannot be modified by anybody who does not possess the secret key. In production, SECRET_KEY should be set to a securely randomized string. You can easily generate one using Python by opening a REPL (running python in your terminal) and entering:  
```python
>>> import binascii
>>> import os
>>> binascii.hexlify(os.urandom(24))
```
Examples of how to set SQLALCHEMY_DATABASE_URI can be seen [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/ "Flask-Sqlalchemy documentation").  
**Configuration sample to use your Gmail account's email server.**  
```
MAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=True
```
The security features in your Gmail account may prevent the application from sending emails through it unless you explicitly allow "less secure apps" access to your Gmail account. You can read about this [here](https://support.google.com/accounts/answer/6010255?hl=en), and if you are   concerned about the security of your account, you can create a secondary account that you configure just for newsletters emails. 

6. Initialize database.  
```flask create-db```  
7. Create all roles.  
```flask create-roles```  
8. Create the first admin to access the admin panel.  
```flask create-admin```  
9. Run the application.  
```flask run```  
10. Open your web-browser at [http://127.0.0.1:5000/login], you should be redirected to the login page.  
