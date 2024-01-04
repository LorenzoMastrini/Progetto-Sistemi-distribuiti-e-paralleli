import sqlite3
import werkzeug
from __main__ import app
from database.init_db import connect_to_db
from flask import jsonify, request

SEATS = "A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 B1 B2 B3 B4 B5 B6 B7 B8 B9 B10 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 H1 H2 H3 H4 H5 H6 H7 H8 H9 H10 I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 J1 J2 J3 J4 J5 J6 J7 J8 J9 J10"

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
            user["id"] = i["user_id"]
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

        user["id"] = row["user_id"]
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

        cur.execute("INSERT INTO film (name, duration, plot, director, img_url, genre) VALUES (?, ?, ?, ?, ?, ?)", (film_info["name"], film_info["duration"], film_info["plot"], film_info["director"], film_info["imgUrl"], film_info["genres"]))
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

        cur.execute("SELECT name FROM film WHERE name = ?", (schedule_info["film"],))
        film = cur.fetchone()

        if film is None:
            return 1

        cur.execute("SELECT * FROM schedule WHERE movie_time = ?", (schedule_info["movieTime"],))
        schedule_already_existing = cur.fetchone()

        if schedule_already_existing is not None:
            return 2
    
        cur.execute("INSERT INTO schedule (movie_time, film, seats_available) VALUES (datetime(?), ?, ?)", (schedule_info["movieTime"], schedule_info["film"], SEATS))
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

def get_schedules():                            #funzione per ritornare tutti gli orari
    schedules = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM schedule")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            schedule = {}
            schedule["scheduleId"] = i["id"]
            schedule["movieTime"] = i["movie_time"]
            schedule["film"] = i["film"]
            seats_string = str(i["seats_available"])
            schedule["seatsAvailable"] = seats_string.split(' ')

            schedules.append(schedule)
    except:
        schedules = []

    return schedules 

def get_all_orders():
    orders = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, movie_time, reservation.user_id, n_seats, email FROM reservation, users WHERE reservation.user_id = users.user_id")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            order = {}
            order["orderId"] = i["id"]
            order["movieTime"] = i["movie_time"]
            order["userId"] = i["user_id"]
            order["seats"] = i["n_seats"]
            order["email"] = i["email"]

            orders.append(order)
    except:
        orders = []

    return orders 

def change_admin(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,))   
        row = cur.fetchone()
        if(row["is_admin"] == 0):
            cur.execute("UPDATE users SET is_admin = 1 WHERE user_id = ?", (user_id,))
        else:
             cur.execute("UPDATE users SET is_admin = 0 WHERE user_id = ?", (user_id,))   
        
        conn.commit()

        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))   
        row = cur.fetchone()
        user["userId"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["password"] = row["password"]
        user["isAdmin"] = row["is_admin"]       
    except:
        conn.rollback()
    finally:
        conn.close()    

    return user 

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
    
@app.route('/api/admin/films/delete/<film_id>', methods=['DELETE'])           #route a cui il client fa richiesta per eliminare un film
def api_delete_film(film_id):
    return jsonify(delete_film(film_id))
    
@app.route('/api/admin/films/schedule/add-schedule', methods=['POST'])                #route a cui il client fa richiesta per aggiungere un orario
def api_add_schedule():
    schedule_info = request.get_json()
    result = add_schedule(schedule_info)
    if result == 1:
        return handle_bad_request("Film non esistente")
    elif result == 2:
        return handle_bad_request("Sala occupata")
    else:
        return jsonify(result)

@app.route('/api/admin/films/schedule/delete/<id>', methods=['DELETE'])      #route a cui il client fa richiesta per eliminare un orario
def api_delete_schedule(id):
    return jsonify(delete_schedule(id))

@app.route('/api/admin/films/schedule/update', methods=['PUT'])             #route a cui il client fa richiesta per aggiornare un orario
def api_update_schedule():
    update = request.get_json()
    result = update_schedule(update)
    return jsonify(result)

@app.route('/api/admin/films/schedule/get-schedules', methods=['GET'])      #route a cui il client fa richiesta per prendere tutti gli orari
def api_get_schedules():
    return jsonify(get_schedules())

@app.route('/api/admin/users/<user_id>', methods=['GET'])                     #route a cui il client fa richiesta per vedere un utente specifico
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/admin/users', methods=['GET'])                               #route a cui il client fa richiesta per vedere tutti gli utenti
def api_get_users():
    return jsonify(get_users())

@app.route('/api/admin/users/delete/<user_id>', methods=['DELETE'])           #route a cui il client fa richiesta per eliminare un utente
def api_delete_users(user_id):
    return jsonify(delete_users(user_id))

@app.route('/api/admin/users/orders', methods=['GET'])                         #route a cui il client fa richiesta per prendere le prenotazioni di tutti gli utenti
def api_get_all_orders():
    return jsonify(get_all_orders())

@app.route('/api/admin/users/change-admin/<user_id>', methods=['PUT'])         #route a cui il client fa richiesta per promuovere o declassare un utente
def api_create_admin(user_id):
    return jsonify(change_admin(user_id))

