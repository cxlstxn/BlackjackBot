import sqlite3
import datetime

CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, balance INTEGER, playertotal INTEGER, dealertotal INTEGER, playercards TEXT, dealercards TEXT, playersuits TEXT, dealersuits TEXT, acecount INTEGER, bet INTEGER, gameactive TEXT, lastpayed TEXT);'
INSERT_ROW = 'INSERT INTO users(username, balance, playertotal, dealertotal, playercards, dealercards, playersuits , dealersuits, acecount, bet, gameactive, lastpayed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
GET_ALL_NAMES = 'SELECT username FROM users;'

def connect():
    return sqlite3.connect('data.db')

def create_tables(connection):
    with connection:
        connection.execute(CREATE_USER_TABLE)
        
def add_row(connection, name):
    with connection:
        connection.execute(INSERT_ROW, (name, 10000, 0, 0,"", "", "", "", 0, 0, "False", str(datetime.datetime.now())))

def get_all_names(connection):
    with connection:
        x = connection.execute(GET_ALL_NAMES)
        return x

def set_player_cards(connection, name, cards):
    with connection:
        connection.execute('UPDATE users SET playercards = ? WHERE username = ?', (cards, name))

def set_dealer_cards(connection, name, cards):
    with connection:
        connection.execute('UPDATE users SET dealercards = ? WHERE username = ?', (cards, name))

def set_player_total(connection, name, total):
    with connection:
        connection.execute('UPDATE users SET playertotal = ? WHERE username = ?', (total, name))

def set_dealer_total(connection, name, total):
    with connection:
        connection.execute('UPDATE users SET dealertotal = ? WHERE username = ?', (total, name))

def get_active(connection, name):
    with connection:
        x = connection.execute('SELECT gameactive FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]
    
def set_game_active(connection, name, active):
    with connection:
        connection.execute('UPDATE users SET gameactive = ? WHERE username = ?', (active, name))

def set_player_suits(connection, name, suits):
    with connection:
        connection.execute('UPDATE users SET playersuits = ? WHERE username = ?', (suits, name))

def set_dealer_suits(connection, name, suits):
    with connection:
        connection.execute('UPDATE users SET dealersuits = ? WHERE username = ?', (suits, name))

def get_player_cards(connection, name):
    with connection:
        x = connection.execute('SELECT playercards FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_dealer_cards(connection, name):
    with connection:
        x = connection.execute('SELECT dealercards FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_player_total(connection, name):
    with connection:
        x = connection.execute('SELECT playertotal FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_dealer_total(connection, name):
    with connection:
        x = connection.execute('SELECT dealertotal FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_game_active(connection, name):
    with connection:
        x = connection.execute('SELECT gameactive FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_player_suits(connection, name):
    with connection:
        x = connection.execute('SELECT playersuits FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_dealer_suits(connection, name):
    with connection:
        x = connection.execute('SELECT dealersuits FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def get_ace_count(connection, name):
    with connection:
        x = connection.execute('SELECT acecount FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def set_ace_count(connection, name, count):
    with connection:
        connection.execute('UPDATE users SET acecount = ? WHERE username = ?', (count, name))

def get_bet(connection, name):
    with connection:
        x = connection.execute('SELECT bet FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]

def set_bet(connection, name, bet):
    with connection:
        connection.execute('UPDATE users SET bet = ? WHERE username = ?', (bet, name))

def get_balance(connection, name):
    with connection:
        x = connection.execute('SELECT balance FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]
    
def set_balance(connection, name, bal):
    with connection:
        connection.execute('UPDATE users SET balance = ? WHERE username = ?', (bal, name))

def get_last_payed(connection, name):
    with connection:
        x = connection.execute('SELECT lastpayed FROM users WHERE username = ?', (name,))
        return x.fetchone()[0]
    
def set_last_payed(connection, name, time):
    with connection:
        connection.execute('UPDATE users SET lastpayed = ? WHERE username = ?', (time, name))