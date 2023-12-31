import sqlite3
import hashlib
from __main__ import app
from database.init_db import connect_to_db
from flask import jsonify, request, session
from routers.admin_router import get_user_by_id
from app import handle_bad_request

def registration(registration_info):                #funzione per la registrazione di un utente
    inserted_user = {}
    row = [] 
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = ?", (registration_info["email"],))
        row = cur.fetchone()

        if row is not None:
            return 400
            
        password_hash = hashlib.sha256(registration_info["password"].encode('utf-8')).hexdigest()
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (registration_info["name"], registration_info["email"], password_hash))
        conn.commit()
 
        inserted_user = get_user_by_id(cur.lastrowid)
        return inserted_user 
    except:     
        conn.rollback()
    finally:
        conn.close()

def login(login_info):                              #funzione per verificare l'esito del login dell'utente
    user = {}
    try:
        session.pop("email", None)

        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        password_hash = hashlib.sha256(login_info["password"].encode('utf-8')).hexdigest()

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (login_info["email"], password_hash))     
        row = cur.fetchone()

        if (row["email"] == login_info["email"]) and (row["password"] == password_hash):                 
            user["id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["password"] = row["password"]
            session["email"] = row["email"]
            user["token"] = hashlib.sha256(session["email"].encode('utf-8')).hexdigest()
            user["isAdmin"] = row["is_admin"]

            cur.execute("UPDATE users SET token = ? WHERE user_id = ?", (user["token"], user["id"]))
            conn.commit()

            return user 
    except:
        return 400

def logout():                                                  #funzione per logout: rimuovo l'utente dalla sessione
    message = {}

    session.pop("user", None)
    message["status"] = "Logout"

    return session

def get_orders(token_hash):                                       #funzione per recuperare prenotazioni dell'utente
    orders = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT user_id FROM users WHERE token = ?", (token_hash,))
        row = cur.fetchone()

        cur.execute("SELECT * FROM reservation WHERE user_id = ?", (row[0],))
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            order = {}
            order["id"] = i["id"]
            order["userId"] = i["user_id"]
            order["movieTime"] = i["movie_time"]
            order["seats"] = i["n_seats"]

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

@app.route('/api/users/orders/<token_hash>', methods=['GET'])              #route a cui il client fa richiesta per recuperare prenotazioni
def api_get_orders(token_hash):
    return jsonify(get_orders(token_hash))