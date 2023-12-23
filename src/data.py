import os
import re
import base64
import io
from PIL import Image


def create_image(path, base64_image):
    base64_image = re.sub(r'data:image/(\w+);base64,', '', base64_image).encode()
    image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path, 'webp', save_all=True)
    return path

def get_event_poster_path(asso, title, date):
    asso = re.sub(r'[^\w]+', '-', asso).strip('-')
    title = re.sub(r'[^\w]+', '-', title).strip('-')
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