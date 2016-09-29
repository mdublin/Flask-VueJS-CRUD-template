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

csrf = CsrfProtect()
db = SQLAlchemy()
# end for vue.js


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    #bootstrap.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    db.init_app(app)
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



# this is original app object
#app = Flask(__name__)
#csrf.init_app(app)

# blog.config.DevelopmentConfig is calling to the DevelopmentConfig() class in config.py, a class that contains the SQLAlchemy db URI, etc

#config_path = os.environ.get("CONFIG_PATH", "CRUD.config.DevelopmentConfig")
#print config_path

#app.config.from_object(config_path)





