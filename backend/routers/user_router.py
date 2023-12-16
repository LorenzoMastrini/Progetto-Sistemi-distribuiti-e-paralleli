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
        session.pop("user", None)

        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        password_hash = hashlib.sha256(login_info["password"].encode('utf-8')).hexdigest()

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (login_info["email"], password_hash))     
        row = cur.fetchone()

        if (row["email"] == login_info["email"]) and (row["password"] == password_hash):
            '''if(row["is_admin"] == 0):
                row["is_admin"] = " "

                user["id"] = row["user_id"]
                user["name"] = row["name"]
                user["email"] = row["email"]
                user["password"] = row["password"]
                session["user"] = row["name"]
                user["token"] = session["user"]
                user["isAdmin"] = row["is_admin"]
            elif(row["is_admin"] == 1):
                row["is_admin"] = "True"
                
                user["id"] = row["user_id"]
                user["name"] = row["name"]
                user["email"] = row["email"]
                user["password"] = row["password"]
                session["user"] = row["name"]
                user["token"] = session["user"]
                user["isAdmin"] = row["is_admin"]'''
            
            user["id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["password"] = row["password"]
            session["user"] = row["name"]
            user["token"] = session["user"]
            user["isAdmin"] = row["is_admin"]
            
            return user 
    except:
        return 400

def logout():                                                  #funzione per logout: rimuovo l'utente dalla sessione
    message = {}

    session.pop("user", None)
    message["status"] = "Logout"

    return session

def get_orders(user_id):                                       #funzione per recuperare prenotazioni dell'utente
    orders = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM reservation WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            order = {}
            order["id"] = i["id"]
            order["userId"] = i["user_id"]
            order["movieTime"] = i["movie_time"]
            order["nSeats"] = i["n_seats"]

            orders.append(order)
    except:
        orders = {}

    conn.commit()

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

@app.route('/api/users/orders/<user_id>', methods=['GET'])              #route a cui il client fa richiesta per recuperare prenotazioni
def api_get_orders(user_id):
    return jsonify(get_orders(user_id))