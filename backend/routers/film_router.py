import sqlite3
from __main__ import app
from database.init_db import connect_to_db
from flask import jsonify, request


def get_films():                                            #funzione per recuperare tutti i film nel database
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
            film["imgUrl"] = i["img_url"]
            film["genre"] = i["genre"]
 
            films.append(film)
    except:
        films = []

    return films

def get_film_schedule(film_name):                          #funzione per recuperare gli orari associati ad un film specifico
    schedule = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE film = ?", (film_name,))
        rows = cur.fetchall()

        for i in rows:
            schedule_dic = {}
            schedule_dic["id"] = i["id"]
            schedule_dic["movieTime"] = i["movie_time"]
            schedule_dic["film"] = i["film"]
            seats_string = str(i["seats_available"])
            schedule_dic["seatsAvailable"] = seats_string.split(' ')

            schedule.append(schedule_dic)
    except: 
        schedule = []
    
    return schedule

def get_film_by_name(film_name):                          #funzione per recuperare un film specifico nel database
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
        film["imgUrl"] = row["img_url"]
        film["genre"] = row["genre"]
    except: 
        film = {}
    
    return film

def reserve(reserve_info):                          #funzione per la prenotazione dei posti: aggiorna i posti disponibili nella sala e aggiunge una entry nella tabella reservation
    try:
        conn = connect_to_db()

        cur = conn.cursor()
        cur.execute("SELECT seats_available FROM schedule WHERE movie_time = ?", (reserve_info["movieTime"],))
        
        row = cur.fetchone()
        seats_string = str(row[0])                  #converto in stringa l'elemento contenuto nell'oggetto row
        seats_list = seats_string.split(' ')        #converto in lista la stringa e separo gli elementi in base ad un certo carattere

        reserve_info_seats = str(reserve_info["seats"])                                     #traduzione inversa per quello che viene passato dall'utente
        reserve_info_seats = reserve_info_seats.translate({ord(i): None for i in "[],'"})

        for i in reserve_info["seats"]:             #rimuovo dalla lista dei posti disponibili in sala quelli prenotati dall'utente
            seats_list.remove(i)
        
        cur.execute("UPDATE schedule SET seats_available = ? WHERE movie_time = ?", (" ".join(seats_list), reserve_info["movieTime"]))                                   #aggiorna i nuovi posti disponibili nella sala    
        cur.execute("INSERT INTO reservation (movie_time, user_id, n_seats) VALUES (?, ?, ?)", (reserve_info["movieTime"], reserve_info["userId"], reserve_info_seats))  #aggiunto una nuova prenotazione nella tabella reservation

        conn.commit()    
    except: 
        conn.rollback()
    finally:
        conn.close()    
    
    return reserve_info                             #ritorno le informazioni della prenotazione

@app.route('/api/films', methods=['GET'])                               #route a cui il client fa richiesta per vedere tutti i film nel database
def api_get_films():
    return jsonify(get_films())                                         

@app.route('/api/films/schedule/<film_name>', methods=['GET'])          #route a cui il client fa richiesta per recuperare la schedule di un film specifico
def api_get_film_schedule(film_name):
    return jsonify(get_film_schedule(film_name))                

@app.route('/api/films/<film_name>', methods=['GET'])                   #route a cui il client fa richiesta per recuperare le informazioni su un film specifico
def api_get_film(film_name):
    return jsonify(get_film_by_name(film_name))                                   

@app.route('/api/films/reserve', methods=['POST'])                      #route a cui il client fa richiesta per prenotare il numero di posti che ha scelto
def api_reserve():
    reserve_info = request.get_json()                                   
    return jsonify(reserve(reserve_info))


