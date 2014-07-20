from flask import render_template
from flask import request
from flask import jsonify
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from flask_gzip import Gzip

import flask.ext.sqlalchemy as sqlalchemy

from datetime import datetime

import env
import flask
import os


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
assets = Environment(app)
gzip = Gzip(app)

js = Bundle('js/jquery-1.8.2.min.js', 'js/bootstrap-carousel.js', 'js/es5-shim.min.js', 'js/home.js', output='js/netflix-rate.min.js')

css = Bundle('css/reset.css', 'css/bootstrap.css', 'css/bootstrap-responsive.css', 'css/base.css', output='css/netflix-rate.min.css')

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

  success = False
  user = None

  if uuid and ip_addr:
    try:
      user = User(uuid, ip_addr)
      db.session.add(user)
      db.session.commit()
      user = user.to_dict()
      success = True
    except sqlalchemy.sqlalchemy.exc.IntegrityError:
      user = None

  return jsonify(**{
      'success' : success,
      'user' : user,
      })


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(60), unique=True)
    created_at = db.Column(db.DateTime)
    ip_addr = db.Column(db.String(40), unique=True)

    def __init__(self, uuid, ip_addr):
        self.uuid = uuid
        self.ip_addr = ip_addr
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return str(self.__dict__)

    def to_dict(self):
      return {
          'uuid': self.uuid,
          'ip_addr' : self.ip_addr,
          'created_at' : str(self.created_at)
          }

if __name__ == '__main__':
    app.config.from_pyfile('env.py')
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 7070))
    app.run(host=host, port=port)
