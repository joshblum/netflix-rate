import env
import flask
import os

from flask import render_template
from flask.ext.assets import Environment, Bundle
from flask_gzip import Gzip


app = flask.Flask(__name__)
assets = Environment(app)
gzip = Gzip(app)

js = Bundle('js/jquery-1.8.2.min.js', 'js/bootstrap-carousel.js', 'js/es5-shim.min.js', 'js/home.js', output='js/netflix-rate.min.js')

css = Bundle('css/reset.css', 'css/bootstrap.css', 'css/bootstrap-responsive.css', 'css/base.css', output='css/netflix-rate.min.css')

assets.register('js_all', js)
assets.register('css_all', css)

@app.route("/")
def index():
    return render_template('home.html', title="downloads")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title=404), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', title=500), 500

if __name__ == "__main__":
    app.config.from_pyfile("env.py")
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 7070))
    app.run(host=host, port=port)