#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# for csrf protection
from flask_wtf.csrf import CsrfProtect

from config import config

# for vue.js, allowing for ${} delimiter in html files with jinja2 markup
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='$$',
        block_end_string='$$',
        variable_start_string='$',
        variable_end_string='$',
        comment_start_string='$#',
        comment_end_string='#$',

    ))

#app = CustomFlask(__name__)

# because we are creating an application instance in create_app()
# there is no global application instance object being passed to these
# extensions below.
# When you have an application instance, you complete the initialization
# of these extensions on the app object by passing the app object to 
# extension.init_app(app), like is done in create_app()

# creating unitialized extensions
csrf = CsrfProtect()
db = SQLAlchemy()


def create_app(config_name):
    """
    Create an application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    #bootstrap.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    db.init_app(app)

    # using this context manager block to execute db.create_all(), which
    # maps the table to the db, within the context of the application 
    # instance (app) being pushed or activated in the current application 
    # context using app_context(). In other words, SQLAlchemy now knows what 
    # the current app is. If we do not use this, we get a RunTimeError of:
    # application not registered on db instance and no application bound to
    # current object.
    with app.app_context():
        db.create_all()

    csrf.init_app(app)



    #login_manager.init_app(app)
    #pagedown.init_app(app)
    
    #if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    #    from flask_sslify import SSLify
    #    sslify = SSLify(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #from .auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    #from .api_1_0 import api as api_1_0_blueprint
    #app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    
    return app


