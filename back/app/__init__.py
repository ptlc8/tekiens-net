from flask import Flask, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
import os

from .api import api
from . import ics
from .rss import get_rss


front_dir = '../../front/dist/'


# Main app
app = Flask(__name__, static_folder=front_dir + 'assets')
app.register_blueprint(api, url_prefix='/api')


# ics routes
app.route('/events.ics', methods=['GET'])(ics.get_events)
app.route('/assos/<id>/events.ics', methods=['GET'])(ics.get_asso_events)
app.route('/events/<id>.ics', methods=['GET'])(ics.get_event)


# RSS Feed
app.route('/events.rss')(get_rss)


# Front-end
@app.route('/<path:path>')
@app.route('/', defaults={'path': ''})
def get_front(path):
    if not os.path.exists(front_dir + path):
        path = 'index.html'
    return send_from_directory(front_dir, path)

@app.route('/displayer')
def get_displayer_front():
    return send_from_directory(front_dir, 'displayer.html')


# Data
@app.route('/data/<path:path>')
def get_data(path):
    return send_from_directory('../data', path)


# Fix for reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app)
