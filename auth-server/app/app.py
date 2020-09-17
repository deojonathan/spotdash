"""Main entry point for Flask WSGI app."""
import flask
import flask_cors

_ALLOWED_ORIGINS = (
  "localhost",
)

app = flask.Flask(__name__)
flask_cors.CORS(app, origins=_ALLOWED_ORIGINS)

@app.route('/')
def getHello():
  return 'Hello I am running'
