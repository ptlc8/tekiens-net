import os
import re
import base64
import io
from PIL import Image


def normalize(string):
    return re.sub(r'[^\w]+', '-', string).strip('-')

def create_image(path, base64_image):
    base64_image = re.sub(r'data:image/(\w+);base64,', '', base64_image).encode()
    image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path, 'webp', save_all=True)
    return path

def update_asso_folder(old_name, new_name=None):
    old_name = normalize(old_name)
    new_name = normalize(new_name or old_name)
    if old_name == new_name or not os.path.exists('data/' + old_name):
        return True
    if os.path.exists('data/' + new_name):
        return False
    print('Renaming', old_name, 'to', new_name)
    os.rename('data/' + old_name, 'data/' + new_name)

def get_event_poster_path(asso, title, date):
    asso = normalize(asso)
    title = normalize(title)
    date = re.compile(r'\d{4}-\d{2}-\d{2}').search(str(date)).group()
    return 'data/' + asso + '/' + date + '-' + title + '.webp'

def create_event_poster(asso, title, date, base64_poster):
    path = get_event_poster_path(asso, title, date)
    return create_image(path, base64_poster)
    
def update_event_poster(asso, old_title, old_date, title=None, date=None):
    old_path = get_event_poster_path(asso, old_title, old_date)
    new_path = get_event_poster_path(asso, (title or old_title), (date or old_date))
    if old_path == new_path or not os.path.exists(old_path):
        return old_path
    os.rename(old_path, new_path)
    return new_path
    
def delete_event_poster(asso, title, date):
    path = get_event_poster_path(asso, title, date)
    if os.path.exists(path):
        os.remove(path)
    return path