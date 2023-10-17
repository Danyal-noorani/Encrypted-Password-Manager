import pickle as pk
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import mysql.connector as sql

con = sql.connect(host="localhost", user="root", password="tiger")
cur = con.cursor(buffered=True)

with open('salt.dat', 'rb') as t:
    salt = pk.load(t)

def kdf():
    return PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=480000,
    )

globalUsername = ''
globalFernet = 'Fernet()'


def login(username, passwd):
    global globalUsername, globalFernet, globaKey
    password = bytes(passwd, encoding='utf-8')  # Encodes Password

    key = base64.urlsafe_b64encode(kdf().derive(password))
    globaKey = key

    FernetInstance = Fernet(key)  # Created Fernet Instance
    try:
        cur.execute('USE EPMDatabase')
        cur.execute('SELECT * FROM {}'.format(username))
        initialStatement = cur.fetchone()
        try:
            FernetInstance.decrypt(eval(initialStatement[2]))  # decrypts passsword from userfile
            globalUsername = username
            globalFernet = FernetInstance
            return True
        except:
            return False

    except:
        try:
            cur.execute('CREATE DATABASE EPMDatabase')
        except:
            pass
        cur.execute('USE EPMDatabase')
        cur.execute('CREATE TABLE {}(Name VARCHAR(50),Username TEXT(200000),Password TEXT(20000))'.format(username))
        statement = FernetInstance.encrypt(b'Initial Statement')
        cur.execute('INSERT INTO {} VALUES("Initializing_Key",NULL,"{}")'.format(username, statement))
        con.commit()
        return True


def addPassword(name, accountuser, accountpasswd):
    print(type(accountuser))
    accountuser = bytes(accountuser, encoding='utf-8')
    accountpasswd = bytes(accountpasswd, encoding='utf-8')
    accountuser  = globalFernet.encrypt(accountuser)
    accountpasswd = globalFernet.encrypt(accountpasswd)
    cur.execute('INSERT INTO {} VALUES("{}","{}","{}")'.format(globalUsername, name, accountuser, accountpasswd))
    con.commit()


def readpasswords():
    cur.execute('SELECT * FROM {}'.format(globalUsername))
    data = cur.fetchall()
    data.pop(0)
    lst = []
    for i in data:
        du = globalFernet.decrypt(eval(i[1]))
        dp = globalFernet.decrypt(eval(i[2]))
        lst.append([i[0],du.decode(),dp.decode()])
    return lst


def deletePassword(name):
    cur.execute('DELETE FROM {} WHERE Name = "{}"'.format(globalUsername,name))
    con.commit()


def clearData():
    cur.execute('DROP DATABASE EPMDATABASE')