import hashlib
import base64
import sqlite3
import sys
from Crypto.Cipher import AES
from Crypto import Random
import os


db = "dist/pass2.db"

#create new DB, create table stocks
if os.path.isfile(db):
    con = sqlite3.connect(db)
else:
    name = "Youssef"
    con = sqlite3.connect(db)
    name_in = (name,)
    con.execute('''CREATE TABLE passwords ( pid INTEGER primary key, website VARCHAR(50) , password VARCHAR(150) )''')
    con.execute('''CREATE TABLE users ( uid INTEGER primary key, user VARCHAR(50) , pin INTEGER )''')
    con.execute('INSERT INTO users (user,pin) VALUES (?, 6421)', name_in)

c = con.cursor()

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()


    def encrypt(self,raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))


    def decrypt(self,enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

cipher =AESCipher(key='MyKey')

def store_password():
    website = raw_input('Please enter what the password is for? ')
    new_pass = raw_input('Please enter a password: ')
    hashed_password = cipher.encrypt(new_pass)
    input_s = [website, hashed_password]
    c.execute("INSERT INTO passwords (WEBSITE, PASSWORD) VALUES (?,?)", input_s)
    print ("Password has been added successfully!")
    con.commit()


def retrieve_password():
    pin = 0
    cat = ""
    web = raw_input("Who are you? ")
    web_in = (web,)
    c.execute("SELECT * FROM users WHERE user = ? ", web_in)
    exist = c.fetchone()
    if exist is None:
        sys.exit("No user found, Quitting!")
    else:
        pin = raw_input("What is your pin? ")

    if int(pin) == exist[2]:
        print "Identity verified"
        c.execute("SELECT website FROM passwords")
        result = c.fetchall()
        print "Websites that are available: "
        for i in range(0, len(result)):
            print result[i][0]
        cat = raw_input("What website do you need? ")
    else:
        sys.exit("Wrong pin code, Quitting!")
    cat_in = (cat.strip(),)
    c.execute("SELECT password FROM passwords WHERE website= ?", cat_in)
    result = c.fetchone()[0]
    print cipher.decrypt(result)

if __name__ == "__main__":
    valid = False
    while (valid != True):
        decision = raw_input("Do you want to retrieve or store a password? (R/S)? ")
        if decision.strip() == 'S':
            valid = True
            store_password()
        elif decision.strip() == 'R':
            valid = True
            retrieve_password()
        else:
            print "Please enter a valid symbol!"
    raw_input("Press Enter to Quit!")






#old_pass = raw_input('Now please enter the password again to check: ')
#if check_password(hashed_password, old_pass):
 #   print('You entered the right password')
#else:
  #  print('I am sorry but the password does not match')