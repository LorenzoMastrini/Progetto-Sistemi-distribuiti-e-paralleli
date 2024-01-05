import werkzeug
from flask import Flask                                                       
from flask_cors import CORS         #consente di richiedere risorse da una pagina web al server che si trova in un dominio esterno                         
import os

app = Flask(__name__)               #inizializzazione app

import routers.admin_router         #importo i file in cui sono suddivise le funzioni e route dell'API utilizzate dal client
import routers.film_router
import routers.user_router

app.secret_key = os.urandom(24)    
CORS(app, resources={r"/*": {"origins": "*"}})

@app.errorhandler(werkzeug.exceptions.BadRequest)     #definisco una funzione per gestire eventuali errori che può far tornare il server
def handle_bad_request(e):
    return e, 400

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)                             #avvio l'applicazione server