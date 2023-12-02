import sqlite3
import click
from flask import current_app, g # current_app punta all'applicazione Flask che sta gestendo la richiesta
# g: oggetto speciale unico oer ogni richiesta usato per memorizzare dati
# che possono essere richiesti da più funzioni durante la richiesta
# La connessione è salvata e riusata invece che crearne una nuova se get_db
# viene cvìhiamata una seconda volta nella stessa richiesta

def get_db():
    if 'db' not in g:
        # stabilisce una connessione al file puntato dalla chiave di configurazione DATABASE
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # dice alla connessione di tornare righe che si comportano come dizionari, per accedere alle colonne tramite nome
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db() # torna una connessione al db, usata per eseguire i comandi letti dal file 'schema.sql'

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db') # definisce il comando 'init-db' a linea di comando per inizializzare il database
def init_db_command():
    # Clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')

# registriamo le funzioni 'close_db' e 'init_db_command' con l'istanza dell'applicazione per poter essere usate da essa
def init_app(app):
    app.teardown_appcontext(close_db) # dice a Flask di chiamare 'close_db' per pulure dopo il return della risposta
    app.cli.add_command(init_db_command) # aggiunge un nuovo comando chiamabile col comando 'flask'
