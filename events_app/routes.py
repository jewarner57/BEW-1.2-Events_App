"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest, EventType

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def index():
    """Show upcoming events to users!"""

    # Gets all events and sends them to the template
    events = Event.query.all()

    return render_template('index.html', events=events)


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    # Gets the event with the given id and sends it to the template
    event = Event.query.filter_by(id=event_id).one()

    return render_template('event_detail.html', event=event)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # Gets the event with the given id from the database
    event = Event.query.filter_by(id=event_id).one()

    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')

    if is_returning_guest:
        # Looks up the guest by name, and adds the event to their
        # events_attending, then commits to the database
        guest = Guest.query.filter_by(name=guest_name).one()

        guest.events_attending.append(event)

        db.session.add(guest)
        db.session.commit()

    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')
        # Creates a new guest with the given name, email, and phone, and
        # adds the event to their events_attending, then commits to the database

        newGuest = Guest(name=guest_name, email=guest_email, phone=guest_phone)
        newGuest.events_attending.append(event)

        db.session.add(newGuest)
        db.session.commit()

    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        eventType = request.form.get('type')

        try:
            date_and_time = datetime.strptime(f'{date} {time}',
                                              '%Y-%m-%d %H:%M')
        except ValueError:
            print('there was an error: incorrect datetime format')

        # Creates a new event with the given title, description, &
        # datetime, then adds and commits it to the database

        newEvent = Event(title=new_event_title,
                         description=new_event_description,
                         date_and_time=date_and_time,
                         event_type=eventType)
        db.session.add(newEvent)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html', eventTypes=EventType)


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # Gets the guest with the given id and sends it to the template
    guest = Guest.query.filter_by(id=guest_id).one()

    return render_template('guest_detail.html', guest=guest)
