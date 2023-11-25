from flask import Flask, send_from_directory

from api import api


app = Flask(__name__, static_folder='front/dist/assets')
app.register_blueprint(api, url_prefix='/api')


# Front-end

@app.route('/<path:path>')
def get_front(path):
    if path.split('/')[-1].find('.') == -1:
        path = 'index.html'
    return send_from_directory('front/dist', path)

@app.route('/')
def get_index():
    return send_from_directory('front/dist', 'index.html')
