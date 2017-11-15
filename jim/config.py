"""
JIM protocol config file.
"""

# ************************************
# * Explicit is better than implicit *
# ************************************
# # Keys
# ACTION = 'action'
# TIME = 'time'
# TYPE = 'type'
# USER = 'user'
# ACCOUNT_NAME = 'account_name'
# PASSWORD = 'password'
# TO = 'to'
# FROM = 'from'
# MESSAGE = 'message'
# ROOM = 'room'
# RESPONSE = 'response'
# ALERT = 'alert'
# ERROR = 'error'
#
# # Values
# PRESENCE = 'presence'
# PROBE = 'probe'
# MSG = 'msg'
# QUIT = 'quit'
# JOIN = 'join'
# LEAVE = 'leave'
# AUTHENTICATE = 'authenticate'
# STATUS = 'status'  # also is key for USER

# Response codes
BASIC_NOTICE = 100
IMPORTANT_NOTICE = 101
OK = 200
CREATED = 201
ACCEPTED = 202
WRONG_REQUEST = 400  # or JSON object
NOT_AUTHORIZED = 401
WRONG_LOGIN_OR_PASSWORD = 402
FORBIDDEN = 403
NOT_FOUND = 404
CONFLICT = 409
GONE = 410
SERVER_ERROR = 500