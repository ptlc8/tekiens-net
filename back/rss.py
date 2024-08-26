from datetime import timezone
from enum import Enum
from mimetypes import guess_type
from os import environ
from flask import Response, request, current_app
from feedgen.feed import FeedGenerator
from markdown import markdown
from api.database import get_db
from api.events import parse_event

def parse_base_url(base_url: str) -> str:
    if base_url.endswith('/'):
        return base_url[:-1]
    return base_url

def fetch_events() -> list:
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
       SELECT events.id, title, events.description as description, poster, date, createDate, asso_id, names as asso_names
       FROM events
       INNER JOIN assos ON events.asso_id = assos.id
   ''')
    events = [parse_event(event) for event in cursor.fetchall()]
    return events

def generate_feed(events: list) -> FeedGenerator:
    base_url = parse_base_url(request.url_root)

    feed = FeedGenerator()
    feed.load_extension('dc')
    feed.title('Événements - Tekiens.net')
    feed.description('Liste des événements Tekiens.net')
    feed.link([
        { 'href': f'{base_url}/events' },
        { 'href': f'{base_url}/events.rss', 'rel': 'self' }
    ])
    feed.language('fr')
    feed.logo(f'{base_url}/assets/icons/192x192.png')

    for event in events:
        entry_link = f'{base_url}/events/{event["id"]}'

        entry = feed.add_entry()
        entry.title(event['title'])
        entry.link(href=entry_link)
        entry.dc.dc_creator(event['asso_names'].split(',')[0])
        # Dates are stored in UTC in the database
        entry.published(event['date'].replace(tzinfo=timezone.utc))
        entry.guid(entry_link)

        if event['poster'] is not None:
            entry.enclosure(url=base_url+event['poster'], type=guess_type(event['poster'])[0], length=0)

        if event['description'] is not None:
            entry.content(markdown(event['description']), type='CDATA')

    return feed

def get_rss() -> Response:
    events = fetch_events()
    feed = generate_feed(events)
    return Response(feed.rss_str(pretty=current_app.debug), mimetype='application/rss+xml')
