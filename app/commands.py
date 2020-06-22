'''

Defines application CLI.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

from click import command
from flask import current_app
from flask.cli import with_appcontext

from .extensions import db
from .models import User, Role


@command(name='create-db')
@with_appcontext
def create_tables():
    '''Create tables described in models.'''

    db.create_all()


@command(name='drop-db')
@with_appcontext
def drop_tables():
    '''Delete tables described in models.'''

    db.drop_all()


@command(name='create-roles')
@with_appcontext
def create_roles():
    '''Create all the roles necessary for the application to work.'''

    admin = Role(
        name='Admin',
        description='Site administrator'
    )
    tutor = Role(
        name='Tutor',
        description='Can all that can student plus creating and editing posts'
    )
    student = Role(
        name='Student',
        description='Can read posts, leave comments, send messages'
    )
    db.session.add_all((admin, tutor, student))
    db.session.commit()


@command(name='create-admin')
@with_appcontext
def create_admin():
    '''
    Create a site administrator from .env file. Note that in another case
    it will not be possible to assign it except through the CLI
    '''

    admin = User(
        username=current_app.config['ADMIN_USERNAME'],
        email=current_app.config['ADMIN_EMAIL'],
        password=current_app.config['ADMIN_PASSWORD']
    )
    db.session.add(admin)
    db.session.commit()
    admin.roles.append(Role.query.filter_by(name='Admin').first())
    db.session.add(admin)
    db.session.commit()


commands = (
    create_tables,
    drop_tables,
    create_roles,
    create_admin
)
