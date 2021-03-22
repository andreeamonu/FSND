#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import babel
import pytz
import dateutil.parser
from datetime import datetime
from flask_babel import Babel
from flask import (
Flask, 
render_template, 
request, 
Response, 
flash, 
redirect, 
url_for
)
from flask_moment import Moment
from flask_sqlalchemy import  SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from sqlalchemy.orm import load_only
from models import (
  app, 
  db, 
  Venue, 
  Artist, 
  Show
)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

#----------------------------------------------------------------------------#
# Models are available in models.py
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
#  Venues
#----------------------------------------------------------------------------#

@app.route('/venues')
def venues():
  venues = Venue.query.all()
# Defining data to be used as a list for the city and state values
  data = []
  venue_places = set()

  for venue in venues:
    # Add tuple for location
    venue_places.add((venue.city, venue.state)) 

  for venue_location in venue_places:
    venues_data=[]
    for venue in venues:
      if (venue.city == venue_location[0] and venue.state == venue_location[1]):
        shows = db.session.query(Show).join(Venue, Show.venue_id==Venue.id)
        upcoming_shows_count = 0 # set initial number of upcoming shows to 0
        for show in shows:
          if show.start_time > datetime.now():
            upcoming_shows_count += 1
        venues_data.append({
          "id": venue.id,
          "name": venue.name,
          "upcoming_shows_count": upcoming_shows_count
        })

    data.append({
      "city": venue_location[0],
      "state": venue_location[1],
      "venues": venues_data
      })
   
  return render_template('pages/venues.html', areas=data)

# Search for venues based on string search

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '').strip()
  # ilike used for insensitive search
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []

  for venue in venues:
    shows = db.session.query(Show).join(Venue, Show.venue_id==Venue.id)
    # attempted use of loops for upcoming shows 
    upcoming_shows_count = 0
    for show in shows:
      if show.start_time > datetime.now():
        upcoming_shows_count += 1
    data.append({
      "id": venue.id,
      "name": venue.name,
      "upcoming_shows_count": upcoming_shows_count
    })

  response={
    "count": len(venues),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  # User error case
  if not venue:
    flash('Venue with venue ID ' + venue.id + ' does not exist.')
  else:
    shows = db.session.query(Show).join(Venue, Show.venue_id==Venue.id)
    # Queries for past and upcoming shows
    past_shows = []
    past_shows_count = 0
    upcoming_shows = []
    upcoming_shows_count = 0
    # Get shows details
    for show in shows:
      if show.start_time < datetime.now(): 
        past_shows_count += 1
        past_shows.append({
          "artist_id": show.artist.id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": format_datetime(str(show.start_time))
          })
      if show.start_time > datetime.now(): 
        upcoming_shows_count += 1
        upcoming_shows.append({
          "artist_id": show.artist.id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": format_datetime(str(show.start_time))
          })

  venue_data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": upcoming_shows_count
    }

  return render_template('pages/show_venue.html', venue=venue_data)

# Edit Venue

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

# Retreive existing details
  venue_data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }

  return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  form = VenueForm()
  # Update with new details
  try:
    venue = Venue.query.get(venue_id)
    venue.name=form.name.data,
    venue.genres=form.genres.data,
    venue.address=form.address.data,
    venue.city=form.city.data,
    venue.state=form.state.data,
    venue.phone=form.phone.data,
    venue.website=form.website.data,
    venue.facebook_link=form.facebook_link.data,
    venue.seeking_talent=form.seeking_talent.data,
    venue.seeking_description=form.seeking_description.data,
    venue.image_link=form.image_link.data

    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + form.name.data + ' has not been updated.')
  else:
    flash('Venue ' + form.name.data + ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Venue

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  
  name = form.name.data.strip()
  genres = form.genres.data
  address = form.address.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  phone = form.phone.data
  website = form.website.data.strip()
  facebook_link = form.facebook_link.data.strip()
  seeking_talent = True if form.seeking_talent.data == 'Yes' else False # allows for user interaction and correct database completion
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()

  error = False

  try:
    new_venue = Venue(name=name, genres=genres, address=address, city=city, state=state, phone=phone, website=website, facebook_link=facebook_link, seeking_talent=seeking_talent, seeking_description=seeking_description,image_link=image_link)
    db.session.add(new_venue)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/venues.html')

#  Delete Venue

@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  venue = Venue.query.get(venue_id)

  error = False

  try:
    for show in venue.shows:
      db.session.delete(show) # any shows associated with the venue will be deleted
    db.session.delete(venue)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    return render_template("500.html"), 500
  else:
    flash('Venue was successfully deleted!')
    return render_template('pages/venues.html')

#----------------------------------------------------------------------------#
# Artists.
#----------------------------------------------------------------------------#

@app.route('/artists')
def artists():
  data = []
  artists = Artist.query.all()

  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

# Search for artists based on  search - similar to venue search

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  data = []
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()  #ilike allows for insensitive searches

  for artist in artists:
    shows = db.session.query(Show).join(Artist, Artist.id==Show.artist_id)
    # attempted use of loops for upcoming shows 
    upcoming_shows_count = 0
    for show in shows:
      if show.start_time > datetime.now():
        upcoming_shows_count += 1
    data.append({
      "id": artist.id,
      "name": artist.name,
      "upcoming_shows_count": upcoming_shows_count
    })

  response = {
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

# Shows the artist for the given artist_id

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if not artist:
    flash('Artist with artist ID ' + artist.id + ' does not exist.') # user error

  else:
    shows = db.session.query(Show).join(Artist, Artist.id==Show.artist_id)
    # Queries for past and upcoming shows
    past_shows = []
    past_shows_count = 0
    upcoming_shows = []
    upcoming_shows_count = 0
    for show in shows:
      if show.start_time < datetime.now():
        past_shows_count += 1
        past_shows.append({
          "venue_id": show.venue.id,
          "venue_name": show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": format_datetime(str(show.start_time))
        })
      if show.start_time > datetime.now():
        upcoming_shows_count += 1
        upcoming_shows.append({
          "venue_id": show.venue.id,
          "venue_name": show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": format_datetime(str(show.start_time))
        })

  artist_data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": upcoming_shows_count
    }

  return render_template('pages/show_artist.html', artist=artist_data)

# Edit Artist

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  artist_data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
    }

  return render_template('forms/edit_artist.html', form=form, artist=artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST']) # same logic as venue/{venue_id}/edit
def edit_artist_submission(artist_id):
  error = False
  form = ArtistForm()

  try:
    artist = Artist.query.get(artist_id)
    artist.name=form.name.data.strip(),
    artist.genres=form.genres.data,
    artist.city=form.city.data.strip(),
    artist.state=form.state.data,
    artist.phone=form.phone.data,
    artist.website=form.website.data.strip(),
    artist.facebook_link=form.facebook_link.data.strip(),
    artist.seeking_venue=form.seeking_venue.data,
    artist.seeking_description=form.seeking_description.data.strip(),
    artist.image_link=form.image_link.data.strip()
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + form.name.data + ' has not been updated.')
  else:
    flash('Artist ' + form.name.data + ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  form = ArtistForm()
  name = form.name.data.strip()
  genres = form.genres.data
  city = form.city.data.strip()
  state = form.state.data
  phone = form.phone.data
  website = form.website.data.strip()
  facebook_link = form.facebook_link.data.strip()
  seeking_venue = True if form.seeking_venue.data == 'Yes' else False
  seeking_description = form.seeking_description.data.strip()
  image_link = form.image_link.data.strip()

  try:
    new_artist = Artist(name=name, genres=genres, city=city, state=state, phone=phone, website=website, facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description, image_link=image_link)
    db.session.add(new_artist)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  else:
    flash('Artist ' + name + ' was successfully listed!')
    
  return render_template('pages/artists.html')

#  Delete Artist

@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  error = False
  artist = Artist.query.get(artist_id)
  try:
    for show in artist.shows:
      db.session.delete(show) # any show associated with the parent will be deleted if the parent is deleted
    db.session.delete(artist)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + name + ' could not be deleted.')
    return render_template("500.html"), 500
  else:
    flash('Artist ' + name+ ' was successfully deleted!')
  
  return render_template('pages/artists.html')

#----------------------------------------------------------------------------#
# Shows
#----------------------------------------------------------------------------#

@app.route('/shows')
def shows():
# Read all shows
  data = []
  shows = Show.query.all()

  for show in shows:
    data.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(str(show.start_time))
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

# Create Shows

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
# using Show form values to Create new shows
  form = ShowForm()

  artist_id = form.artist_id.data.strip()
  venue_id = form.venue_id.data.strip()
  start_time = form.start_time.data

  error = False

  try:
    new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(new_show)
    db.session.commit()
  except():
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash('An error occurred. Show  could not be listed.')
  else:
    flash('Show was successfully listed!')

  return render_template('pages/shows.html')

#----------------------------------------------------------------------------#
# Sorted artists and venues - attempt at going the extra mile
#----------------------------------------------------------------------------#
  # artist_data = []
  # venue_data = []
  # artist = Artist.query.all()
  # venue = Venue.query.all()
  # artists = db.session.query(Artist).order_by(Artist.id.desc()).limit(10).all()
  # venues = db.session.query(Venue).order_by(Venue.id.desc()).limit(10).all()

  # for artist in artists:
  #   artist_data.append({
  #     "id": artist.id,
  #     "name": artist.name
  #   })

  # for venue in venues:
  #   venue_data.append({
  #     "id": venue.id,
  #     "name": venue.name
  #   }) 

#   HTML code:
#   <div class="row">
#     <h4> Recently created Fyyur Artists 🔥</h4>
#         <ul id="lists">
#             {% for artist in artist_data %}
#         <li>
#             <input id="artist_id" value="{{ artist.id }}">
#             <a href="/artist/{{ artist.id }}">{{ artist.name }}</a>
#         </li>
#         {% endfor %}
#     </ul>
#     <h4> Recently created Fyyur Venues 🔥</h4>
#         <ul id="lists">
#             {% for venue in venue_data %}
#         <li>
#             <input id="venue_id" value="{ venue.id }}">
#             <a href="/venue/{{ venue.id }}">{{ venue.name }}</a>
#         </li>
#         {% endfor %}
#     </ul>
# </div>


#----------------------------------------------------------------------------#
# Errors
#----------------------------------------------------------------------------#

@app.errorhandler(401)
def not_found_error(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def not_found_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(422)
def not_found_error(error):
    return render_template('errors/404.html'), 422

@app.errorhandler(405)
def not_found_error(error):
    return render_template('errors/404.html'), 405

@app.errorhandler(409)
def not_found_error(error):
    return render_template('errors/404.html'), 409

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

# # Default port:
# if __name__ == '__main__':
#     app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
