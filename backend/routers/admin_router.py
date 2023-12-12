import sqlite3
import werkzeug
from __main__ import app
from database.init_db import connect_to_db
from flask import jsonify, request

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

def add_film(film_info):                         #funzione per aggiungere film al DB
    inserted_film = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT * FROM film WHERE name = ?", (film_info["name"],)) 
        row = cur.fetchone()

        if row is not None:
            return 400

        cur.execute("INSERT INTO film (name, duration, plot, director) VALUES (?, ?, ?, ?)", (film_info["name"], film_info["duration"], film_info["plot"], film_info["director"]))
        conn.commit()

        return inserted_film
    except:
        conn.rollback() 
    finally:
        conn.close()

def delete_film(film_id):                         #funzione per eliminare un film nel DB                        
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM schedule WHERE film = ?", (film_id,))
        cur.execute("DELETE FROM film WHERE name = ?", (film_id,))
        conn.commit()

        message["status"] = "Film deleted successfully"
    except:
        conn.rollback() 
        message["status"] = "Cannot delete film"
    finally:
        conn.close()

    return message

def add_schedule(schedule_info):                #funzione per aggiungere un nuovo orario al DB
    inserted_schedule = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT * FROM schedule WHERE time = ? AND room_id = ?", (schedule_info["time"], schedule_info["room_id"]))
        row = cur.fetchone()

        if row is not None:
            return 400
        
        cur.execute("SELECT n_seats FROM room WHERE id = ?", (schedule_info["room_id"],))
        row = cur.fetchone()
        cur.execute("INSERT INTO schedule (time, room_id, film, seats_available) VALUES (datetime(?), ?, ?, ?)", (schedule_info["time"], schedule_info["room_id"], schedule_info["film"], row["n_seats"]))
        conn.commit()
        
        return inserted_schedule
    except:
        conn.rollback() 
    finally:
        conn.close()    

def delete_schedule(time):                         #funzione per eliminare un orario dal DB                        
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM schedule WHERE time = ?", (time,))
        conn.commit()

        message["status"] = "Schedule deleted successfully"
    except:
        conn.rollback() 
        message["status"] = "Cannot delete schedule"
    finally:
        conn.close()

    return message

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return e, 400

@app.route('/api/admin/films/add-film', methods=['POST'])                    #route a cui il client fa richiesta per aggiungere un film
def api_add_film():
    film_info = request.get_json()
    result = add_film(film_info)
    if result == 400:
        return handle_bad_request("Film già esistente")
    else:
        return jsonify(result)
    
@app.route('/api/admin/films/schedule/add-schedule', methods=['POST'])                #route a cui il client fa richiesta per aggiungere un orario
def api_add_schedule():
    schedule_info = request.get_json()
    result = add_schedule(schedule_info)
    if result == 400:
        return handle_bad_request("Sala occupata")
    else:
        return jsonify(result)

@app.route('/api/admin/users/<user_id>', methods=['GET'])                     #route a cui il client fa richiesta per vedere un utente specifico
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/admin/users', methods=['GET'])                               #route a cui il client fa richiesta per vedere tutti gli utenti
def api_get_users():
    return jsonify(get_users())

@app.route('/api/admin/users/delete/<user_id>', methods=['DELETE'])           #route a cui il client fa richiesta per eliminare un utente
def api_delete_users(user_id):
    return jsonify(delete_users(user_id))

@app.route('/api/admin/films/delete/<film_id>', methods=['DELETE'])           #route a cui il client fa richiesta per eliminare un film
def api_delete_film(film_id):
    return jsonify(delete_film(film_id))

@app.route('/api/admin/films/schedule/delete/<time>', methods=['DELETE'])              #route a cui il client fa richiesta per eliminare un orario
def api_delete_schedule(time):
    return jsonify(delete_schedule(time))