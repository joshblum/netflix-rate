import env
import flask
import os

from flask import render_template

app = flask.Flask(__name__)

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