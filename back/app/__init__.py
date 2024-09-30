from flask import Flask, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from .api import api
from . import ics
from .rss import get_rss


app = Flask(__name__, static_folder='../../front/dist/assets')
app.register_blueprint(api, url_prefix='/api')


# ics routes
app.route('/events.ics', methods=['GET'])(ics.get_events)
app.route('/assos/<id>/events.ics', methods=['GET'])(ics.get_asso_events)

# RSS Feed
app.route('/events.rss')(get_rss)

# Front-end
@app.route('/<path:path>')
def get_front(path):
    if path.split('/')[-1].find('.') == -1:
        path = 'index.html'
    return send_from_directory('../../front/dist', path)

@app.route('/')
def get_index():
    return send_from_directory('../../front/dist', 'index.html')

@app.route('/displayer')
def get_displayer_front():
    return send_from_directory('../../front/dist', 'displayer.html')

# Data
@app.route('/data/<path:path>')
def get_data(path):
    return send_from_directory('../data', path)


# Fix for reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app)
