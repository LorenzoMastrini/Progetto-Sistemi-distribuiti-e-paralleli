import sqlite3
from database.config_db import connect_to_db
from flask import Flask, jsonify
from flask_cors import CORS

def get_films():                                            #funzione che interroga il DB e restituisce la lista di tutti i film in un dictionary
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

def get_film_schedule(film_name):                          #funzione per che interroga il DB e restituisce la programmazione riguardante un film specifico in un dictionary
    schedule = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE film = ?", (film_name,))
        rows = cur.fetchall()

        for i in rows:
            schedule_dic = {}
            schedule_dic["time"] = i["time"]
            schedule_dic["room_id"] = i["room_id"]
            schedule_dic["film"] = i["film"]

            schedule.append(schedule_dic)
    except: 
        schedule = []
    
    return schedule

def get_film(film_name):                          #funzione per che interroga il DB e restituisce la programmazione riguardante un film specifico in un dictionary
    film = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM film WHERE name = ?", (film_name,))
        row = cur.fetchone()

        film["name"] = row["name"]
        film["duration"] = row["duration"]
        film["plot"] = row["plot"]
        film["director"] = row["director"]

    except: 
        film = {}
    
    return film


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/films', methods=['GET'])
def api_get_films():
    return jsonify(get_films())                                 #ritorno l'output della funzione get_film() in JSON per l'invio dei dati

@app.route('/api/schedule/<film_name>', methods=['GET'])        #route a cui il client fa richiesta con metodo GET per vedere la schedule di un film specifico
def api_get_film_schedule(film_name):
    return jsonify(get_film_schedule(film_name))                #ritorno l'output della funzione get_film_schedule() in JSON per l'invio dei dati

@app.route('/api/films/<film_name>', methods=['GET'])           #route a cui il client fa richiesta con metodo GET per vedere sia le info sul film che la programmazione
def api_get_film(film_name):
    film_info = []

    film_info.append(get_film(film_name))
    film_info.append(get_film_schedule(film_name))
    return jsonify(film_info)                                   #in una lista inserisco l'output delle funzioni get_film() e get_film_schedule() e ritorno il JSON della lista
    

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    #app.run()