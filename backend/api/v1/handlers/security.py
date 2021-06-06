# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from typing import Optional
from datetime import datetime, timedelta

from jwt import PyJWTError, decode as jwt_decode, encode as jwt_encode

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import (
    OAuth2,
    OAuthFlowsModel,
    get_authorization_scheme_param,
)

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from starlette.requests import Request

import httplib2
from oauth2client import client
from google.oauth2 import id_token
from google.auth.transport import requests

from core.schemas.security import User, TokenData, Token
from core.config import (
    API_DOMAIN,
    API_PORT,
    SECRET_KEY,
    ALGORITHM,
    GOOGLE_CLIENT_SECRETS_JSON,
    GOOGLE_CLIENT_ID,
    ACCESS_TOKEN_EXPIRE_MIN,
)


security_router = APIRouter(prefix="", redirect_slashes=True, tags=["auth"])

API_LOCATION = f"http://{API_DOMAIN}:{API_PORT}"
SWAP_TOKEN_ENDPOINT = "/api/v1/swap_token"
SUCCESS_ROUTE = "/api/v1/users/me"
ERROR_ROUTE = "/api/v1/login_error"
google_login_javascript_server = f"""<!DOCTYPE html>
<html itemscope itemtype="http://schema.org/Article">
<head>
    <meta charset="UTF-8">
    <title>Google Login</title>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js">
    </script>
    <script src="https://apis.google.com/js/client:platform.js?onload=start" async defer>
    </script>
    <script>
    function start() {{
      gapi.load('auth2', function() {{
        auth2 = gapi.auth2.init({{
          client_id: '{GOOGLE_CLIENT_ID}',
          // Scopes to request in addition to 'profile' and 'email'
          // scope: 'additional_scope'
        }});
      }});
    }}
  </script>
</head>
<body>
<button id="signinButton">Sign in with Google</button>
<script>
  $('#signinButton').click(function() {{
    // signInCallback defined in step 6.
    auth2.grantOfflineAccess().then(signInCallback);
  }});
</script>
<script>
function signInCallback(authResult) {{
  if (authResult['code']) {{

    // Hide the sign-in button now that the user is authorized, for example:
    $('#signinButton').attr('style', 'display: none');

    // Send the code to the server
    $.ajax({{
      type: 'POST',
      url: '{API_LOCATION}{SWAP_TOKEN_ENDPOINT}',
      // Always include an `X-Requested-With` header in every AJAX request,
      // to protect against CSRF attacks.
      headers: {{
        'X-Requested-With': 'XMLHttpRequest',
        'X-Google-OAuth2-Type': 'server'
      }},
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {{
          location.href = '{API_LOCATION}{SUCCESS_ROUTE}'
        // Handle or verify the server response.
      }},

      processData: false,
      data: authResult['code']

    }});
  }} else {{
    // There was an error.
    console.log(e)
    location.href = '{API_LOCATION}{ERROR_ROUTE}'
  }}
}}
</script>

</body>
</html>"""
fake_users_db = {
    "nemuku": {
        "username": "nemuku",
        "full_name": "Aleksei Deviatkin",
        "email": "nemuku@gmail.com",
        "disabled": False,
    },
    "devyatkin.dev": {
        "username": "devyatkin.dev",
        "full_name": "Aleksei Deviatkin",
        "email": "devyatkin.dev@gmail.com",
        "disabled": False,
    },
}


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        # cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        # cookie_scheme, cookie_param = get_authorization_scheme_param(
        #     cookie_authorization
        # )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        # elif cookie_scheme.lower() == "bearer":
        #     authorization = True
        #     scheme = cookie_scheme
        #     param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


# oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")


def get_user_by_email(db, email: str):
    for username, value in db.items():
        if value.get("email") == email:
            user_dict = db[username]
            return User(**user_dict)


def authenticate_user_email(fake_db, email: str):
    user = get_user_by_email(fake_db, email)
    if not user:
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     # TODO: read from token header
#     credentials_exception = HTTPException(
#         status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
#     )
#     try:
#         payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except PyJWTError:
#         raise credentials_exception
#     user = get_user_by_email(fake_users_db, email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@security_router.get("/google_login_server", tags=["security"])
def google_login_server():
    return HTMLResponse(google_login_javascript_server)


@security_router.post(f"{SWAP_TOKEN_ENDPOINT}", response_model=Token, tags=["security"])
async def swap_token(request: Request = None):
    # if not request.headers.get("X-Requested-With"):
    #     raise HTTPException(status_code=400, detail="Incorrect headers")

    google_client_type = request.headers.get("X-Google-OAuth2-Type")

    if google_client_type == "server":
        try:
            body_bytes = await request.body()
            auth_code = jsonable_encoder(body_bytes)

            credentials = client.credentials_from_clientsecrets_and_code(
                GOOGLE_CLIENT_SECRETS_JSON, ["profile", "email"], auth_code
            )

            http_auth = credentials.authorize(httplib2.Http())

            email = credentials.id_token["email"]

        except:
            raise HTTPException(
                status_code=400, detail="Unable to validate social login"
            )

    if google_client_type == "client":
        body_bytes = await request.body()
        auth_code = jsonable_encoder(body_bytes)

        try:
            idinfo = id_token.verify_oauth2_token(
                auth_code, requests.Request(), GOOGLE_CLIENT_ID
            )

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ValueError("Wrong issuer.")

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            if idinfo["email"] and idinfo["email_verified"]:
                email = idinfo.get("email")

            else:
                raise HTTPException(
                    status_code=400, detail="Unable to validate social login"
                )

        except:
            raise HTTPException(
                status_code=400, detail="Unable to validate social login"
            )

    authenticated_user = authenticate_user_email(fake_users_db, email)

    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect email address")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )

    token = jsonable_encoder(access_token)

    response = JSONResponse({"access_token": token, "token_type": "bearer"})

    print({"access_token": token, "token_type": "bearer"})

    # response.set_cookie(
    #     COOKIE_AUTHORIZATION_NAME,
    #     value=f"Bearer {token}",
    #     domain=API_DOMAIN,
    #     httponly=True,
    #     max_age=1800,
    #     expires=1800,
    # )
    return response


@security_router.get(f"{ERROR_ROUTE}", tags=["security"])
async def login_error():
    return "Something went wrong logging in!"


# @security_router.get("/logout", tags=["security"])
# async def route_logout_and_remove_cookie():
#     # TODO: invalidate token
#     response = RedirectResponse(url="/")
#     return response


# @security_router.get("/users/me/", response_model=User, tags=["users"])
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @security_router.get("/users/me/items/", tags=["users"])
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
