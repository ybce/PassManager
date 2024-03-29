import hashlib
import base64
import sqlite3
import sys
from Crypto.Cipher import AES
from Crypto import Random

#Connecting and
db = "pass.db"
#create new DB, create table stocks
con = sqlite3.connect(db)
#con.execute('''CREATE TABLE passwords ( pid INTEGER primary key, website VARCHAR(50) , password VARCHAR(150) )''')
c = con.cursor()

#Encryption/Decryption class
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

#Initializing cipher object
cipher =AESCipher(key='MyKey')

#Check if a string represents an int
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#Method that allows user to store a new password
def store_password(user):
    website = raw_input('Please enter what the password is for? ')
    new_pass = raw_input('Please enter a password: ')
    hashed_password = cipher.encrypt(new_pass)
    input_s = [website, hashed_password, user]
    c.execute("INSERT INTO passwords (WEBSITE, PASSWORD, USER) VALUES (?,?,?)", input_s)
    print ("Password has been added successfully!")
    con.commit()

#Method that takes user through retrieving a password
def retrieve_password(user):
    cat = raw_input("What website do you need? ")
    db_in = [cat,user]
    c.execute("SELECT password FROM passwords WHERE website= ? AND user = ? ", db_in)
    result = c.fetchone()[0]
    print cipher.decrypt(result)


#Allows user to decide whether he wants to store or retrieve passwords
def decision(user):
    valid = False
    while (valid != True):
        decision = raw_input("Do you want to retrieve or store a password? (R/S)? ")
        if decision.strip() == 'S':
            valid = True
            store_password(user)
        elif decision.strip() == 'R':
            valid = True
            retrieve_password(user)
        else:
            print "Please enter a valid symbol!"


#Main method: Logs in the user or allows you to create a new user
if __name__ == "__main__":
    pin = 0
    cat = ""
    password = ""
    web = raw_input("Who are you? (Type New to create a user)")
    if web != "New":
        web_in = (web,)
        c.execute("SELECT * FROM users WHERE user = ? ", web_in)
        exist = c.fetchone()[2]
        if exist is None:
            sys.exit("No user found, Quitting!")
        else:
            print "User found"
            pin = raw_input("Please enter your pincode: ")
            if cipher.encrypt(pin) == exist:
                print "Identity verified"
                decision(web)
            else:
                sys.exit("Wrong pin code, Quitting!")
    elif web == "New":
        user = raw_input("Please enter your username: ")
        flag = False
        while(flag != True):
            password = raw_input("Please enter a 4-digit pincode: ")
            if (len(password.strip()) == 4) & (RepresentsInt(password.strip())):
                flag = True
            else:
                print "Invalid Pincode"
        input2_s = [user, cipher.encrypt(password)]
        c.execute("INSERT INTO users (user, pin) VALUES (?,?)", input2_s)
        print "User has been added"
        decision(user)


























#old_pass = raw_input('Now please enter the password again to check: ')
#if check_password(hashed_password, old_pass):
 #   print('You entered the right password')
#else:
  #  print('I am sorry but the password does not match')