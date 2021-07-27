import hashlib
import os

users = {} # A simple demo storage

# Add a user
username = 'guest' # The users username
password = 'florida' # The users password

salt = os.urandom(32) # A new salt for this user
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
users[username] = { # Store the salt and key
    'salt': salt,
    'key': key
}
