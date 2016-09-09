from CRUD import app
from flask import Markup
import mistune as md

# both of these decorated functions are having data/arguments passed to them via the the Jinja filter statemnts in the macros.html file 

@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True))

@app.template_filter()
def dateformat(date, format):
    print date, format
    if not date:
        return None
    return date.strftime(format)


