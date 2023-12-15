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
            user["userId"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["password"] = i["password"]
            user["isAdmin"] = i["is_admin"]

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

        user["userId"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["password"] = row["password"]
        user["isAdmin"] = row["is_admin"]
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

        cur.execute("SELECT * FROM schedule WHERE movie_time = ?", (schedule_info["movieTime"],))
        row = cur.fetchone()

        if row is not None:
            return 400
        
        cur.execute("INSERT INTO schedule (movie_time, film) VALUES (datetime(?), ?)", (schedule_info["movieTime"], schedule_info["film"]))
        conn.commit()
        
        inserted_schedule = get_schedule_by_id(cur.lastrowid)
        return inserted_schedule
    except:
        conn.rollback() 
    finally:
        conn.close()
            
def get_schedule_by_id(schedule_id):                        #funzione per vedere un orario specifico nel DB         
    schedule = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule WHERE id = ?", (schedule_id,))
        row = cur.fetchone()

        schedule["scheduleId"] = row["id"]
        schedule["movieTime"] = row["movie_time"]
        schedule["film"] = row["film"]
        schedule["seatsAvailable"] = row["seats_available"]
    except: 
        schedule = {}
    
    return schedule

def delete_schedule(id):                         #funzione per eliminare un orario dal DB                        
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM schedule WHERE id = ?", (id,))
        conn.commit()

        message["status"] = "Schedule deleted successfully"
    except:
        conn.rollback() 
        message["status"] = "Cannot delete schedule"
    finally:
        conn.close()

    return message

def update_schedule(update):                    #funzione per aggiornare un orario
    updated_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE schedule SET movie_time = ?, film = ? WHERE id = ?", (update["movieTime"], update["film"], update["id"]))
        conn.commit()
        updated_schedule = get_schedule_by_id(update["id"])
    except:
        conn.rollback() 
    finally:
        conn.close()

    return updated_schedule    

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

@app.route('/api/admin/films/schedule/delete/<id>', methods=['DELETE'])      #route a cui il client fa richiesta per eliminare un orario
def api_delete_schedule(id):
    return jsonify(delete_schedule(id))

@app.route('/api/admin/films/schedule/update', methods=['PUT'])         #route a cui il client fa richiesta per aggiornare un orario
def api_update_schedule():
    update = request.get_json()
    result = update_schedule(update)
    return jsonify(result)