import hashlib
import os

users = {} # A simple demo storage

# Add a user
username = 'Brent' # The users username
password = 'spaceCamper101%' # The users password

salt = os.urandom(32) # A new salt for this user
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
users[username] = { # Store the salt and key
    'salt': salt,
    'key': key
}

# Verification attempt 1 (incorrect password)
username = 'Brent'
password = 'spaceCamper101%'

salt = users[username]['salt'] # Get the salt
key = users[username]['key'] # Get the correct key
print(type(salt))
new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

print(key == new_key)
