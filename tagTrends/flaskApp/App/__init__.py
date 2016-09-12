'''Sept 1, 2016
    Flask support for tag trends functionality
    Author: Beth Dellea
'''

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from App import views

