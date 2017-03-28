#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g
from app import db, login_manager
from flask_login import current_user
import base64

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import login_view, register_view, logout_view, dashboard_view
from app.modules.users.models import Users
from app.modules.auth import auth_page




# ----- FLASK LOGIN SPECIAL REQUESTS  -----
@auth_page.before_request
def get_current_user():
    g.user = current_user
    
# Set user_loader callback for session
# which Flask-Login uses to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # return Users.query.filter(Users.id == user_id)
    return Users.query.get(int(user_id))



# Set user_loader callback for token header
# which Flask-Login uses to reload the user object from the user ID stored in token header
@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('Authorization')
    # first, try to login using the token url arg
    if token is None:
        token = request.args.get('token')

    # next, try to login using Basic Auth
    if token is not None:
        token = token.replace('Basic ', '', 1)
        try:
            token = base64.b64decode(token)
        except TypeError:
            pass
        
        username,password = token.split(":") # naive token

         # password decoding  when remote app client
        if request.is_xhr == True :
            form.password.data = base64.b64decode(form.password.data).decode('UTF-8')
            
        user = Users.query.filter_by(username=username).first()
        if (user is not None):            
            if (user.check_password(password)):
                return user
    # finally, return None if both methods did not login the user
    return None