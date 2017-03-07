import hashlib
import base64
import sys
import pymongo
import random
import string
import pyperclip
from pymongo import MongoClient
from Crypto.Cipher import AES
from Crypto import Random
import os


client = MongoClient()
db = client.test
users = db.users
passwords = db.passwords

PASSWORD_CHARSET =  string.ascii_letters+string.digits


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

def gen_random_string(char_set, length):
        if not hasattr(gen_random_string, "rng"):
            gen_random_string.rng = random.SystemRandom()  # Create a static variable
        return ''.join([gen_random_string.rng.choice(char_set) for _ in xrange(length)])




#Method that allows user to store a new password
def store_password(user):
    website = raw_input('Please enter what the password is for? ')
    generate = raw_input('Do you want to generate a password for '+website+'? (Y/N) ')
    if generate.strip() == 'Y':
        new_pass = gen_random_string(PASSWORD_CHARSET, 10)

    elif generate.strip() == 'N':
        new_pass = raw_input('Please enter a password: ')

    else:
        print "A password has been created for you!"
        new_pass = gen_random_string(PASSWORD_CHARSET, 10)

    hashed_password = cipher.encrypt(new_pass)
    input_s = [website, hashed_password, user]
    #insert password with user given
    passwords.insert_one({
        "website":website,
        "password": hashed_password,
        "user":user
        })
    print ("Password has been added successfully!")


#Method that takes user through retrieving a password
def retrieve_password(user):
    user_in = (user,)
    #fetch all websites and display them
    print "Your websites are:"
    for w in passwords.find({"user":user}):
        print w["website"]
    cat = raw_input("What website do you need? ")
    #fetch password needed and display it
    p = passwords.find_one({"user":user, "website":cat.strip()},{"password":1})
    pyperclip.copy(cipher.decrypt(p['password']))
    print "Your password has been added to the clipboard!"


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
    user_input = raw_input("Who are you? (Type New to create a new user) ")
    if user_input.strip().upper() != "NEW":
        web_in = (user_input.strip(),)
        #check if user and pin match
        user = users.find_one({"user":user_input}, {"user":1})
        #print user['user']
        exist = users.find_one({"user":user_input},{"pincode":1})
        #print exist['pincode']

        if user is None:
            sys.exit("No user found, Quitting!")
        else:
            print "User found"
            pin = raw_input("Please enter your pincode: ")

            if pin.strip() == cipher.decrypt(exist['pincode']):
                print "Identity verified"
                decision(user_input)
            else:
                sys.exit("Wrong pin code, Quitting!")
    elif user_input.strip().upper() == "NEW":
        user = raw_input("Please enter your username: ")
        flag = False
        while(flag != True):
            password = raw_input("Please enter a 4-digit pincode: ")
            if (len(password.strip()) == 4) & (RepresentsInt(password.strip())):
                flag = True
            else:
                print "Invalid Pincode"

        #insert new user and pincode into collection
        users.insert_one({
            "user":user,
            "pincode":cipher.encrypt(password.strip())
        })

        print "User has been added"
        decision(user)


























#old_pass = raw_input('Now please enter the password again to check: ')
#if check_password(hashed_password, old_pass):
 #   print('You entered the right password')
#else:
  #  print('I am sorry but the password does not match')