# Description
Education platform for students and tutors written on Flask. 

# How to run?
1. Clone or download this repository  
2. Create virtual environment in repository: ```python3 -m venv venv```  
3. Activate virtual environment: ```source venv/bin/activate```  
4. Install requirements: ```python3 -m pip install -r requirements.txt``` 
5. Set up the configuration data in ```.env``` file as shown below:  
```
SECRET_KEY=<Your secret string>

DATABASE_URI=<dialect+driver://username:password@host:port/database>

MAIL_SERVER=<Mail server>
MAIL_PORT=<Mail port>
MAIL_USE_TLS=<True or False>
MAIL_USERNAME=<The part before the @ symbol (local part)>
MAIL_PASSWORD=<Password for $MAIL_USERNAME@$MAIL_SERVER>

ADMIN_EMAIL=no-reply@gmail.com
ADMIN_PASSWORD=<Password for no-reply@gmail.com>
```  
#### Useful links:
[SECRET_KEY](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask "Stackoverflow")  
[SQLALCHEMY_DATABASE_URI](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/ "Flask-Sqlalchemy documentation")  
#### Configuration sample to use your Gmail account's email server. 
```
MAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=True
```
The security features in your Gmail account may prevent the application from sending emails  
through it unless you explicitly allow "less secure apps" access to your Gmail account. You can  
read about this [here](https://support.google.com/accounts/answer/6010255?hl=en), and if you are concerned about the security of your account, you can create  
a secondary account that you configure just for newsletters emails. 

6. Initialize database: ```flask init-db``` 
7. Create all roles: ```flask create-roles```  
8. Create the first admin to access the admin panel: ```flask create-admin```  
9. Run the application: ```flask run```  
10. Open your web-browser at [http://127.0.0.1:5000/login], you should be redirected to the login page.  