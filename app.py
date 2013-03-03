import env
import flask
import os

app = flask.Flask(__name__)

@app.route("/")
def index():
    

    return flask.Response(**res)

if __name__ == "__main__":
    app.config.from_pyfile("env.py")
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8080))
    app.run(host=host, port=port)