import werkzeug
from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

import routers.admin_router
import routers.film_router
import routers.user_router

app.secret_key = os.urandom(24)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return e, 400

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)