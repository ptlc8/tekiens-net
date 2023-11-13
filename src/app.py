from flask import Flask, send_from_directory

from api import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


# Front-end

@app.route('/<path:path>')
def get_front(path):
    return send_from_directory('front/dist', path)

@app.route('/')
def get_index():
    return send_from_directory('front/dist', 'index.html')
