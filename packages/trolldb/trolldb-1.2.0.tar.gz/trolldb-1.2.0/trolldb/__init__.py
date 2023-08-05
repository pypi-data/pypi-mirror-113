import json
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os.path

version = '1.1.0'

class Database:
    def __init__(self, key, filename="troll.trolldb"):
        if len(key) < 0:
            raise Exception("""Key not defined, Usage: Database("key here")""")
        try:
            self.key = bytes(key, 'utf-8')
        except:
            raise Exception("Invalid, generate a key with trolldb.genkey()")
        self.filename = filename
        if not os.path.isfile(filename):
            open(filename, 'wb').write(Fernet(self.key).encrypt(b"{}"))
        else:
            try:
                key = Fernet(self.key)
                str(key.decrypt(open(self.filename, 'rb').read()), 'utf-8')
            except InvalidToken:
                raise Exception("Wrong key defined.")
    def getkey(self):
        return self.key
    def getfilename(self):
        return self.filename
    def add(self, name, value):
        key = Fernet(self.key)
        d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
        d[name] = value
        with open(self.filename, 'wb') as a:
            a.write(Fernet(self.key).encrypt(bytes(json.dumps(d), 'utf-8')))
    def get(self, name):
        if len(name) < 0:
            raise Exception("Name of the variable not defined")
        key = Fernet(self.key)
        d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
        return d[name]
    def getplainjson(self):
        key = Fernet(self.key)
        return str(key.decrypt(open(self.filename, 'rb').read()), 'utf-8')
    def remove(self, name):
        key = Fernet(self.key)
        d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
        del d[name]
        with open(self.filename, 'wb') as a:
            a.write(Fernet(self.key).encrypt(bytes(json.dumps(d), 'utf-8')))
class Table:
    class new:
        def __init__(self, db, name):
            self.key = db.getkey()
            self.filename = db.getfilename()
            self.tablename = name
            key = Fernet(self.key)
            d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
            try:
                d[name]
            except:
                d[name] = json.loads("{}")
                with open(self.filename, 'wb') as a:
                    a.write(Fernet(self.key).encrypt(bytes(json.dumps(d), 'utf-8')))
        def add(self, name, value):
            key = self.key 
            d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
            d[self.tablename][name] = value
            with open(self.filename, 'wb') as a:
                a.write(Fernet(self.key).encrypt(bytes(json.dumps(d), 'utf-8')))
        def remove(self, name):
            key = self.key 
            d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
            del d[self.tablename][name]
            with open(self.filename, 'wb') as a:
                a.write(Fernet(self.key).encrypt(bytes(json.dumps(d), 'utf-8')))
        def get(self, name):
            key = self.key 
            d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
            return d[self.tablename][name]
def genkey():
    gk = Fernet.generate_key()
    print(f"your generated key = {gk}, written to key.trolldb")
    open("key.trolldb", 'wb').write(gk)
def key_by_filename(filename):
    return open(filename,'r').read()