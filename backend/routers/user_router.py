import sqlite3
import hashlib
from __main__ import app
from database.init_db import connect_to_db
from flask import jsonify, request, session
from routers.admin_router import get_user_by_id
from app import handle_bad_request

def registration(registration_info):                     #funzione per la registrazione di un utente
    inserted_user = {}
    row = [] 
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = ?", (registration_info["email"],))       #controllo se un utente registrato con l'email inserita nel form già esiste
        row = cur.fetchone()

        if row is not None:
            return 400
            
        password_hash = hashlib.sha256(registration_info["password"].encode('utf-8')).hexdigest()   #la password all'interno del database non viene inserita in chiaro, ma viene prima crittata con un algoritmo di hash e poi memorizzata
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (registration_info["name"], registration_info["email"], password_hash))
        conn.commit()
 
        inserted_user = get_user_by_id(cur.lastrowid)
        return inserted_user                                                                        #ritorno l'utente inserito 
    except:     
        conn.rollback()
    finally:
        conn.close()

def login(login_info):                                      #funzione per verificare l'esito del login dell'utente
    user = {}
    try:
        session.pop("email", None)                          #inizializzo la variabile di sessione

        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        password_hash = hashlib.sha256(login_info["password"].encode('utf-8')).hexdigest()    #eseguo l'hashing della password inserita nel form di login che verrà confrontata con quella nel database

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (login_info["email"], password_hash))   #recupero l'utente con le informazioni inserite nel form di login 
        row = cur.fetchone()

        if (row["email"] == login_info["email"]) and (row["password"] == password_hash):       #se i dati nell'oggetto sono uguali ai dati passati dall'utente il login ha successo           
            user["id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["password"] = row["password"]
            session["email"] = row["email"]
            user["token"] = hashlib.sha256(session["email"].encode('utf-8')).hexdigest()     #tra le informazioni dell'utente è presente anche un token che viene utilizzato in alcune route in modo tale da non passare l'id dell'utente in chiaro sull'URL
            user["isAdmin"] = row["is_admin"]

            cur.execute("UPDATE users SET token = ? WHERE user_id = ?", (user["token"], user["id"]))
            conn.commit()

            return user                                                                       #ritorno l'utente che ha fatto il login
    except:
        return 400

def logout():                                                  #funzione per logout
    message = {}

    session.pop("user", None)                                  #rimuovo l'utente dalla sessione
    message["status"] = "Logout"

    return session

def get_orders(token_hash):                                    #funzione per recuperare prenotazioni dell'utente
    orders = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT user_id FROM users WHERE token = ?", (token_hash,))     #attraverso il token recupero l'id dell'utente 
        row = cur.fetchone()

        cur.execute("SELECT reservation.id, user_id, schedule.film, reservation.movie_time, reservation.n_seats FROM reservation, schedule WHERE user_id = ? AND reservation.movie_time = schedule.movie_time", (row[0],))
        rows = cur.fetchall()

        for i in rows:
            order = {}
            order["id"] = i["id"]
            order["userId"] = i["user_id"]
            order["movieTime"] = i["movie_time"]
            order["seats"] = i["n_seats"]
            order["film"] = i["film"]

            orders.append(order)
    except:
        orders = {}

    return orders                                       
        
@app.route('/api/users/registration', methods=['POST'])                 #route a cui il client fa richiesta per registrare un utente
def api_registration():
    registration_info = request.get_json()
    result = registration(registration_info)
    if result == 400:
        return handle_bad_request("Email già esistente")
    else:
        return jsonify(result)

@app.route('/api/users/login', methods=['POST'])                        #route a cui il client fa richiesta per fare il login
def api_login():
    login_info = request.get_json()
    result = login(login_info)
    if result == 400:
        return handle_bad_request("Email o password errati")
    else:    
        return jsonify(result)

@app.route('/api/users/logout', methods=['GET'])                        #route a cui il client fa richiesta per fare il logout
def api_logout():
    return jsonify(logout())

@app.route('/api/users/orders/<token_hash>', methods=['GET'])              #route a cui il client fa richiesta per recuperare le sue prenotazioni
def api_get_orders(token_hash):
    return jsonify(get_orders(token_hash))