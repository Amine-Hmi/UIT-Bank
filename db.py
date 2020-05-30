import sqlite3
#import uuid
import hashlib
import os


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,customer text,amount integer,operation text,balance integer,sender INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS USERS(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username text, password text, rib text, acc_type text, balance integer)")
        self.conn.commit()

    def fetch(self,username):
        self.cur.execute("SELECT username,acc_type,balance,rib FROM users where username= ?",[username])
        rows = self.cur.fetchall()
        return rows
    
    def fetch_users(self):
        self.cur.execute("SELECT username,rib from users")
        rows = self.cur.fetchall()
        return rows

    def insert(self, part, customer, retailer, price):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?, ?, ?)",
                         (part, customer, retailer, price))
        self.conn.commit()

    def add_user(self, username, password,tp,bal):
        #rib = uuid.uuid1()
        rib = int.from_bytes(os.urandom(5), byteorder='little') % 99999999999
        #code password in sha256
        password = hashlib.sha256(str(password).encode()).hexdigest()
        #RIB {2}CODE BANQUE, {6}CODE AGENCE, {11}N°_COMPTE, {2}CLE
        self.cur.execute("SELECT username FROM USERS WHERE USERNAME = ?",[username])
        res = self.cur.fetchone()
        if (res):
            return 'Error'
        else:
            self.cur.execute("INSERT INTO users (username,password,rib,acc_type,balance) VALUES (?, ?, ?, ?, ?)",
                                 (username, password, str(rib),tp,bal))
            self.conn.commit()
    
    def remove_user(self,rib):
        self.cur.execute("DELETE from users where rib = ?",
        [str(rib)])
        self.conn.commit()

    def withdraw (self,amount,rib):
        self.cur.execute("update users set balance = balance - ? where rib = ?",
        (amount,rib))
        self.conn.commit()

    def deposit (self,amount,rib):
        self.cur.execute("update users set balance = balance + ? where rib = ?",
        (amount, rib))
        self.conn.commit()
    
    def add_transaction (self,rib,amount,operation,balance,sender):
        self.cur.execute("insert into transactions (customer,amount,operation,balance,sender) VALUES (?, ?, ?, ?, ?) ",
        (rib,amount, operation, balance,sender))
        self.conn.commit()

    def user_fetch_transactions(self,rib):
        self.cur.execute("select id,customer,operation, amount, balance, created_at ,sender from TRANSACTIONS WHERE customer = ?",[rib])
        res = self.cur.fetchall()
        return res
    
    def user_fetch(self, username, password):
        match = hashlib.sha256(str(password).encode()).hexdigest()
        self.cur.execute("SELECT * FROM users WHERE username= ? and password= ?",
                        (str(username), str(match)))
        found = self.cur.fetchone()
        if found:
            return ('Logged in')
        else:
            return ('User Not Found Or Wrong Password !')

    def user_fetch_infos(self, username):
        self.cur.execute("SELECT username, acc_type, rib, balance FROM users WHERE rib= ?"
        , [username])
        found = self.cur.fetchone()
        return (found)

    def remove(self, id):
        self.cur.execute("DELETE FROM users WHERE id=?", (id))
        self.conn.commit()

    def update(self, account, rib):
        self.cur.execute("UPDATE users SET acc_type = ? WHERE rib = ?",
                         (account, str(rib)))
        self.conn.commit()

    def __del__(self):
        self.conn.close()