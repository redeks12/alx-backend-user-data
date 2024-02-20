"""
Main file
"""

from auth import Auth

email = "bob@bob.com"
password = "MyPwdOfBob"
auth = Auth()

auth.register_user(email, password)

sess = auth.create_session(email)
print(sess)
print(auth.destroy_session(1))
print(auth.get_user_from_session_id(sess))

# print(auth)
