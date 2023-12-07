import sqlite3
from database.config_db import connect_to_db
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import hashlib
import os

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

def reserve(reserve_info):                          #funzione per la prenotazione dei posti: invia al DB una query di update per aggiornare i posti disponibili 
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT seats_available FROM schedule WHERE time = ? AND room_id = ?", (reserve_info["time"], reserve_info["room_id"]))
        row = cur.fetchone()

        cur.execute("UPDATE schedule SET seats_available = ? WHERE time = ? AND room_id = ?", (row[0] - reserve_info["n_seats"], reserve_info["time"], reserve_info["room_id"]))
        conn.commit()
    except: 
        conn.rollback()
    finally:
        conn.close()    
    
    return reserve_info

def registration(registration_info):                #funzione per la registrazione di un utente
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        password_hash = hashlib.sha256(registration_info["password"].encode('utf-8')).hexdigest()
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (registration_info["name"], registration_info["email"], password_hash))
        conn.commit()
        
        inserted_user = get_user_by_id(cur.lastrowid)   
    except: 
        conn.rollback()
    finally:
        conn.close() 

    return inserted_user

def get_users():                                    #funzione per vedere tutti gli utenti nel DB                                  
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["password"] = i["password"]
            user["isAdmin"] = i["isAdmin"]

            users.append(user)
    except:
        users = []

    return users

def get_user_by_id(user_id):                        #funzione per vedere un utente specifico nel DB            
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["password"] = row["password"]
        user["isAdmin"] = row["isAdmin"]
    except: 
        user = {}
    
    return user


def delete_users(user_id):                         #funzione per eliminare un utente nel DB                        
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()

        message["status"] = "User deleted successfully"
    except:
        conn.rollback() 
        message["status"] = "Cannot delete user"
    finally:
        conn.close()

    return message

def login(login_info):                              #funzione per verificare l'esito del login dell'utente
    message = {}
    try:
        session.pop("user", None)

        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        password_hash = hashlib.sha256(login_info["password"].encode('utf-8')).hexdigest()
        
        cur = conn.cursor()
        cur.execute("SELECT email, password FROM users WHERE email = ? AND password = ?", (login_info["email"], password_hash))     
        row = cur.fetchone()

        if (row["email"] == login_info["email"]) and (row["password"] == password_hash):
            message["status"] = "Login successfull"
            session["user"] = login_info["email"]

            return message
    except:
        message["status"] = "Login failed"
        
        return message

def logout():                                          #funzione per logout: rimuovo l'utente dalla sessione
    message = {}

    session.pop("user", None)
    message["status"] = "Logout"

    return session

app = Flask(__name__)
app.secret_key = os.urandom(24)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/films', methods=['GET'])
def api_get_films():
    return jsonify(get_films())                                 #ritorno l'output della funzione get_film() in JSON per l'invio dei dati con la HTTP response

@app.route('/api/schedule/<film_name>', methods=['GET'])        #route a cui il client fa richiesta con metodo GET per vedere la schedule di un film specifico
def api_get_film_schedule(film_name):
    return jsonify(get_film_schedule(film_name))                

@app.route('/api/films/<film_name>', methods=['GET'])           #route a cui il client fa richiesta con metodo GET per vedere le informazioni su un film specifico
def api_get_film(film_name):
    return jsonify(get_film(film_name))                                   

@app.route('/api/reserve', methods=['PUT'])                     #route a cui il client fa richiesta con metodo PUT per prenotare il numero di posti che ha scelto
def api_reserve():
    reserve_info = request.get_json()                           #prendo il body della richiesta
    return jsonify(reserve(reserve_info))
        
@app.route('/api/users/registration', methods=['POST'])         #route a cui il client fa richiesta per registrare un utente
def api_registration():
    registration_info = request.get_json()
    return jsonify(registration(registration_info))

@app.route('/api/users/<user_id>', methods=['GET'])             #route a cui il client fa richiesta per vedere un utente specifico
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/users', methods=['GET'])                       #route a cui il client fa richiesta per vedere tutti gli utenti
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])   #route a cui il client fa richiesta per eliminare un utente
def api_delete_users(user_id):
    return jsonify(delete_users(user_id))

@app.route('/api/users/login', methods=['POST'])                #route a cui il client fa richiesta per fare il login
def api_login():
    login_info = request.get_json()
    return jsonify(login(login_info))

@app.route('/api/users/logout', methods=['GET'])                #route a cui il client fa richiesta per fare il logout
def api_logout():
    return jsonify(logout())

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)

