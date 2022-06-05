#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
from datetime import date
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from config import SQLALCHEMY_DATABASE_URI
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# Set up Flask Migrate -me
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #Done -me


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #Done -me

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#Done -me


class Shows(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venu_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    start_time = db.Column(db.DateTime)
    venue = db.relationship('Venue', backref='shows')
    artist = db.relationship('Artist', backref='shows')

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    # Done -me
    venues = Venue.query.all()
    cities = Venue.query.distinct(Venue.city).all()
    data = {
        "venue": venues,
        "city": cities
    }
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    #Done -me

    search_term = request.form.get('search_term')
    searchTerm = "%{}%".format(search_term)
    data = Venue.query.filter(func.lower(Venue.name)
                                  .contains(func.lower(searchTerm))).all()
    count = Venue.query.filter(func.lower(Venue.name)
                               .contains(func.lower(searchTerm))).count()
    response = {
        'data': data,
        'count': count
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    #Done -me

    today = datetime.now()
    venue = Venue.query.get(venue_id)

    past_shows_var = Shows.query.filter(
        Shows.venu_id == venue_id, Shows.start_time < today)
    past_shows = past_shows_var.all()
    past_shows_count = past_shows_var.count()

    upcoming_shows_var = Shows.query.filter(
        Shows.venu_id == venue_id, Shows.start_time >= today)
    upcoming_shows = upcoming_shows_var.all()
    upcoming_shows_count = upcoming_shows_var.count()

    # mutable object
    my_past_shows = []
    my_upcoming_shows = []
    for shows in upcoming_shows:
        aShow = {}
        aShow['start_time'] = shows.start_time
        aShow['artist_id'] = shows.artist_id

        id = shows.artist_id
        artist = Artist.query.get(id)
        name = artist.name
        img = artist.image_link
        aShow['img'] = img
        aShow['artist_name'] = name

        my_upcoming_shows.append(aShow)

    for shows in past_shows:
        aShow = {}
        aShow['start_time'] = shows.start_time
        aShow['artist_id'] = shows.artist_id

        id = shows.artist_id
        artist = Artist.query.get(id)
        name = artist.name
        img = artist.image_link
        aShow['img'] = img
        aShow['artist_name'] = name

        my_past_shows.append(aShow)

    upcoming = {
        'count': upcoming_shows_count,
        'shows': my_upcoming_shows,
        'past_count': past_shows_count,
        'past_shows': my_past_shows,
    }
    return render_template('pages/show_venue.html', venue=venue, upcoming=upcoming)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    #Done -me

    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website_link = request.form['website_link']
    seeking_description = request.form['seeking_description']
    genres = request.form.getlist('genres')

    if request.form.get('seeking_talent', False):
        seeking_talent = True
    else:
        seeking_talent = False

    try:
        new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone,
                          image_link=image_link, facebook_link=facebook_link, website_link=website_link, genres=genres, seeking_description=seeking_description, seeking_talent=seeking_talent)
        db.session.add(new_venue)
        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] +
              ' was successfully listed!')
    except:
        error = True
        db.session.rollback()

        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        #Done -me
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')

    finally:
        db.session.close()

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    #Done -me

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue deleted successfully')
    except:
        error = True
        db.session.rollback()
        flash('Error. Venue could not be deleted')
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    #Done -me

    return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    #Done - me

    data = Artist.query.all()

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    #Done -me

    search_term = request.form.get('search_term')
    searchTerm = "%{}%".format(search_term)
    data = Artist.query.filter(func.lower(
        Artist.name).contains(searchTerm)).all()
    count = Artist.query.filter(func.lower(
        Artist.name).contains(searchTerm)).count()

    response = {
        "data": data,
        'count': count
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    #Done -me

    today = datetime.now()
    artists = Artist.query.get(artist_id)

    past_shows_var = Shows.query.filter(
        Shows.artist_id == artist_id, Shows.start_time < today)
    past_shows = past_shows_var.all()
    past_shows_count = past_shows_var.count()

    upcoming_shows_var = Shows.query.filter(
        Shows.artist_id == artist_id, Shows.start_time >= today)
    upcoming_shows = upcoming_shows_var.all()
    upcoming_shows_count = upcoming_shows_var.count()

    # mutable object
    my_past_shows = []
    my_upcoming_shows = []
    for shows in upcoming_shows:
        aShow = {}
        aShow['start_time'] = shows.start_time
        aShow['artist_id'] = shows.artist_id

        id = shows.venu_id
        venue = Venue.query.get(id)
        name = venue.name
        img = venue.image_link
        aShow['img'] = img
        aShow['venue_name'] = name

        my_upcoming_shows.append(aShow)

    for shows in past_shows:
        aShow = {}
        aShow['start_time'] = shows.start_time
        aShow['artist_id'] = shows.artist_id

        id = shows.venu_id
        venue = Venue.query.get(id)
        name = venue.name
        img = venue.image_link
        aShow['img'] = img
        aShow['venue_name'] = name

        my_past_shows.append(aShow)

    shows = {
        'count': upcoming_shows_count,
        'shows': my_upcoming_shows,
        'past_count': past_shows_count,
        'past_shows': my_past_shows,
    }

    return render_template('pages/show_artist.html', artist=artists, shows=shows)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    # TODO: populate form with fields from artist with ID <artist_id>
    #Done -me
    artist = Artist.query.get(artist_id)
    form = ArtistForm()

    form.process(obj=artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    #Done -me

    artist = Artist.query.get(artist_id)

    if request.form.get('seeking_venue', False):
        seeking_venue = True
    else:
        seeking_venue = False

    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website_link = request.form['website_link']
        artist.seeking_venue = seeking_venue
        artist.seeking_description = request.form['seeking_description']

        db.session.commit()

        flash('Edit was successful!')
    except:
        error = True
        db.session.rollback()

        flash('Edit was unsuccessful!')
    finally:
        db.session()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    #Done -me

    venue = Venue.query.get(venue_id)
    form = VenueForm()

    form.process(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    #Done -me

    venue = Venue.query.get(venue_id)

    if request.form.get('seeking_talent', False):
        seeking_talent = True
    else:
        seeking_talent = False

    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.image_link = request.form['image_link']
        venue.facebook_link = request.form['facebook_link']
        venue.website_link = request.form['website_link']
        venue.genres = request.form.getlist('genres')
        venue.seeking_description = request.form['seeking_description']
        venue.seeking_talent = seeking_talent

        db.session.commit()

        flash('Edit was successful!')
    except:
        error = True
        db.session.rollback()

        flash('Edit was unsuccessful!')
    finally:
        db.session()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    #Done -me

    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website_link = request.form['website_link']
    seeking_description = request.form['seeking_description']
    genres = request.form.getlist('genres')

    if request.form.get('seeking_venue', False):
        seeking_venue = True
    else:
        seeking_venue = False

    try:
        new_artist = Artist(name=name, city=city, state=state, phone=phone,
                            image_link=image_link, facebook_link=facebook_link, website_link=website_link, genres=genres, seeking_description=seeking_description, seeking_venue=seeking_venue)
        db.session.add(new_artist)
        db.session.commit()

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] +
              ' was successfully listed!')
    except:
        error = True
        db.session.rollback()

        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        #Done -me
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')

    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    #Done -me

    try:
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
        flash('Artist deleted successfully')
    except:
        error = True
        db.session.rollback()
        flash('Error. Artist could not be deleted')
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    #Done -me

    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #Done -me

    shows = Shows.query.all()

    my_shows = []

    for show in shows:
        a_show = {}
        id = show.artist_id
        id2 = show.venu_id

        artist = Artist.query.get(id)
        venue = Venue.query.get(id2)
        a_show['artist_name'] = artist.name
        a_show['artist_id'] = id
        a_show['venue_name'] = venue.name
        a_show['venue_id'] = id2
        a_show['venue_img'] = venue.image_link
        a_show['artist_img'] = artist.image_link
        a_show['start_time'] = show.start_time

        my_shows.append(a_show)

    data = my_shows

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    #DOne -me

    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    try:
        new_show = Shows(artist_id=artist_id,
                         venu_id=venue_id, start_time=start_time)
        db.session.add(new_show)
        db.session.commit()

        flash('Show successfully listed')
    except:
        error = True
        db.session.rollback()

        flash('Error. Show could not be listed')
    finally:
        db.session.close()

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/shows/search', methods=['POST'])
def search_shows():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    #Done -me

    search_term = request.form.get('search_term')
    data = Shows.query.filter(Shows.venu_id == search_term).all()
    count = Shows.query.filter(Shows.venu_id == search_term).count()

    venue = Venue.query.get(search_term)

    shows = []
    for i in data:
        a_show = {}
        id = i.artist_id
        artist = Artist.query.get(id)
        a_show['venu_id'] = i.venu_id
        a_show['venu_name'] = venue.name
        a_show['artist_name'] = artist.name
        a_show['artist_id'] = id
        a_show['artist_img'] = artist.image_link
        a_show['venue_img'] = venue.image_link
        a_show['start_time'] = i.start_time
        shows.append(a_show)

    response = {
        'count': count,
        'shows': shows
    }
    return render_template('pages/show.html', results=response, search_term=search_term, venue=venue)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
