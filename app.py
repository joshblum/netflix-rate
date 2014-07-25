from flask import render_template
from flask import request
from flask import jsonify
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from flask_gzip import Gzip

import flask.ext.sqlalchemy as sqlalchemy

from datetime import datetime

import flask
import requests
import os

EMAIL_URL = 'http://u-mail.herokuapp.com/send?to=joshblum@mit.edu&payload=%s'
USER_COUNT = 10000 # send an email every 10k users
DATE_FMT = '%Y-%m-%d %H:%M:%S.%f'

app = flask.Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
assets = Environment(app)
gzip = Gzip(app)

js = Bundle('js/jquery-1.8.2.min.js', 'js/bootstrap-carousel.js',
            'js/es5-shim.min.js', 'js/home.js', output='js/netflix-rate.min.js')

css = Bundle('css/reset.css', 'css/bootstrap.css', 'css/bootstrap-responsive.css',
             'css/base.css', output='css/netflix-rate.min.css')

assets.register('js_all', js)
assets.register('css_all', css)


@app.route('/')
def index():
  return render_template('home.html', title='downloads')


@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html', title=404), 404


@app.errorhandler(500)
def page_not_found(error):
  return render_template('500.html', title=500), 500


@app.route('/track', methods=['POST'])
def track():
  uuid = request.form.get('uuid')
  ip_addr = request.remote_addr
  src = request.form.get('src')

  success = False
  user = None

  if uuid and ip_addr:
    try:
      user = User(uuid, ip_addr, src)
      db.session.add(user)
      db.session.commit()
      user = user.to_dict()
      success = True
      _send_mail()
    except sqlalchemy.sqlalchemy.exc.IntegrityError as e:
      print e
      user = None

  return jsonify(**{
      'success': success,
      'user': user,
  })

def _send_mail():
  user_count = User.query.count()
  if user_count > 0 and not user_count % USER_COUNT:
    payload = '%d unique users.' % user_count
    requests.get(EMAIL_URL % payload)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uuid = db.Column(db.String(60), unique=True)
  created_at = db.Column(db.DateTime)
  ip_addr = db.Column(db.String(40))
  src = db.Column(db.String(10))

  def __init__(self, uuid, ip_addr, src, created_at=None):
    self.uuid = uuid
    self.ip_addr = ip_addr
    self.src = src # chrome or firefox
    if created_at is None:
      self.created_at = datetime.utcnow()
    else:
      try:
        self.created_at = datetime.strptime(created_at, DATE_FMT)
      except ValueErorr as e:
        print e
        self.created_at = datetime.utcnow()

  def __repr__(self):
    return str(self.__dict__)

  def to_dict(self):
    return {
        'uuid': self.uuid,
        'ip_addr': self.ip_addr,
        'src': self.src,
        'created_at': str(self.created_at)
    }

if __name__ == '__main__':
  host = '0.0.0.0'
  port = int(os.environ.get('PORT', 7070))
  app.run(host=host, port=port)
