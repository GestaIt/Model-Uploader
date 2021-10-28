"""
Created by Gestalt on 10/26/21
sessions.py

Handles the caching of session objects.

See for Response object.
https://2.python-requests.org/en/master/user/advanced/#request-and-response-objects

Functions:
    post_with_cross_reference(auth_cookie, request_args) -> Response (see above)
"""

from typing import Any

import requests

cached_sessions: dict[str] = {}


def _get_session(auth_cookie: str) -> requests.Session:
    """Stores request sessions.

    :param auth_cookie: Your Roblox authentication cookie.
    :return: A pre-existing session or a new session.
    """

    if auth_cookie not in cached_sessions.keys():
        session: requests.Session = requests.session()
        session.cookies.update({
            ".ROBLOSECURITY": auth_cookie
        })

        cached_sessions[auth_cookie] = session

        return session
    else:
        return cached_sessions[auth_cookie]


def _get_cross_reference_token(auth_cookie: str) -> str:
    """Gets a new cross reference token affiliated with the Roblox auth cookie.

    :param auth_cookie: Your Roblox authentication cookie.
    :return: A fresh cross reference token.
    """

    session: requests.Session = _get_session(auth_cookie)
    response: requests.Response = session.post("https://auth.roblox.com/v2/logout")

    try:
        token = response.headers["x-csrf-token"]
    except KeyError:
        raise Exception("Please specify a valid auth cookie")

    return token


def post_with_cross_reference(auth_cookie: str, **kwargs: Any) -> requests.Response:
    """Automates the process of getting a new cross reference token and placing it in the headers.

    :param auth_cookie: Your Roblox authentication cookie.
    :param kwargs: Your request arguments.
    :return: A response.
    """

    # Get the token, place it in the headers, and then send the request off!
    session: requests.Session = _get_session(auth_cookie)
    token: str = _get_cross_reference_token(auth_cookie)

    headers = {
        "X-CSRF-TOKEN": token,
        'User-Agent': "Roblox/WinInet"
    }

    return session.post(**kwargs, headers=headers)
