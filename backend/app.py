import sqlite3
from database.config_db import connect_to_db
from flask import Flask, jsonify
from flask_cors import CORS



def get_films():
    films = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM film")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            film = {}
            film["name"] = i["name"]
            film["duration"] = i["duration"]
            film["plot"] = i["plot"]
            film["director"] = i["director"]

            films.append(film)
    except:
        films = []

    return films



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/films', methods=['GET'])
def api_get_films():
    return jsonify(get_films())

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    #app.run()