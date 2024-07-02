from ics import Calendar, Event
from ics.grammar.parse import ContentLine

def add_events_to_calendar(cal, events):
    for event in events:
        asso_name = event['asso'].split(',')[0]
        e = Event()
        e.uid = str(event['id'])
        e.name = '[' + asso_name + '] ' + event['title']
        e.begin = event['date']
        e.location = event['place']
        if event['duration']:
            e.duration = {'minutes': event['duration']}
        e.organizer = asso_name
        e.last_modified = event['lastUpdateDate']
        e.created = event['createDate']
        e.url = event['link']
        #e.status = event['status']
        e.description = event['description']
        e.extra.append(ContentLine('COLOR', {}, event['color']))
        if event['poster']:
            e.extra.append(ContentLine('IMAGE', {}, event['poster']))
        cal.events.add(e)

def create_ics(name, events, color=None):
    cal = Calendar()
    cal.extra.append(ContentLine('X-WR-CALNAME', {}, name))
    cal.extra.append(ContentLine('NAME', {}, name))
    if color:
        cal.extra.append(ContentLine('COLOR', {}, color))
    add_events_to_calendar(cal, events)
    return cal.serialize()