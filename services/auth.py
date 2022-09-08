import os
import logging
import jwt
from flask import abort, jsonify, g, make_response, request
from datetime import timedelta, datetime
from flask_restful import wraps, Resource

from models.user_model import User


def decode_cookie():
    """
    Function to decode cookie and set our api global "cookie" variable with
    what is found in the cookie
    """
    cookie = request.cookies.get("user")

    if not cookie:
        g.cookie = {}
        return

    try:
        g.cookie = jwt.decode(cookie, os.environ["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError as err:
        logging.warning(str(err))
        abort(401)


def set_token_in_cookie(user):
    """
    method to set token with JWT and to send it to cookies
    :param user: user credentials
    :return: validation response
    """
    # encode the user info inside a jwt token
    u = {
        "email": user.email,
        "account": user.account_id,
        "username": user.username,
        "role": user.role,
    }

    token = jwt.encode({"id": user.id, "user": u, "exp": datetime.now() + timedelta(days=30)},
                       os.environ["SECRET_KEY"],
                       algorithm="HS256"
                       )

    # send the token to cookies
    response = make_response(jsonify({
        "status": "success",
        "message": "user logged with success",
        "user": u
    }), 200)
    response.set_cookie("user", token)
    return response


def require_login(func):
    """
    decorator function that checks if a user is logged from the id inside the cookie
    :param func: decorated function
    :return: set cookie "user" as empty if it doesn't match any user id and send a 401, or go through the func
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if "id" is in global cookie
        if "id" not in g.cookie:
            logging.warning("No authorization provided!")
            abort(401)

        # check in db if a user corresponds to the id
        g.user = User.query.get(g.cookie["id"])

        # IF NOT, send a 401 and reset the cookie to empty
        if not g.user:
            response = make_response("", 401)
            response.set_cookie("user", "")
            return response

        # IF YES, validate by returning the decorated func
        return func(*args, **kwargs)
    return wrapper