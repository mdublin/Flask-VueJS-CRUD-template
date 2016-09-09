#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask

# for csrf protection
from flask_wtf.csrf import CsrfProtect


# for vue.js
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

# end for vue.js

# this is original app object
app = Flask(__name__)
csrf.init_app(app)

# blog.config.DevelopmentConfig is calling to the DevelopmentConfig() class in config.py, a class that contains the SQLAlchemy db URI, etc

config_path = os.environ.get("CONFIG_PATH", "CRUD.config.DevelopmentConfig")
print config_path

app.config.from_object(config_path)

#Jinja filters

# views.py contains app.route decorators
from . import views

# filters.py contains two decorated functions —> markdown(text) and dateformat(date, format)
from . import filters

