from flask import Flask

app = Flask(__name__)

from app import admin_views
from app import agent_views
from app import home_views