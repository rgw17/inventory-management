import hashlib
import os
from expiringdict import ExpiringDict
import time
# users = {} # A simple demo storage

# # Add a user
# username = 'spacecamp' # The users username
# password = 'spaceCamper101%' # The users password

# salt = os.urandom(32) # A new salt for this user
# key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
# users[username] = { # Store the salt and key
#     'salt': salt,
#     'key': key
# }

    # password = 'spaceCamper101%' # The users password

    # salt = os.urandom(32) # A new salt for this user
    # key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # user = User(username='spacecamp', salt=salt, key=key)
    # db.session.add(user)
    # db.session.commit()

current_sessions = ExpiringDict(max_len=100, max_age_seconds=2)
current_sessions['one'] = "hello"
time.sleep(1)
print(current_sessions['one'])

