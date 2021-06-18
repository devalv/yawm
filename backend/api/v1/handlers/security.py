# -*- coding: utf-8 -*-
"""Security rest-api handlers."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OpenIdConnect
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import (
    RedirectResponse,
    JSONResponse,
    HTMLResponse,
)
from starlette.requests import Request

import httplib2

from oauth2client import client

from google.oauth2 import id_token
from google.auth.transport import requests

from core.config import (
    ACCESS_TOKEN_EXPIRE_MIN,
    API_DOMAIN,
    API_PORT,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRETS_JSON,
    ALGORITHM,
)
from core.schemas.security import (
    UserDBModel,
    TokenData,
    Token,
)

from core.services.auth import get_current_active_user, create_access_token, get_yoba_active_user


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
  console.log(authResult);
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


@security_router.get("/google_login_server", tags=["security"])
def google_login_server():
    return HTMLResponse(google_login_javascript_server)


@security_router.post(f"{SWAP_TOKEN_ENDPOINT}", response_model=Token, tags=["security"])
async def swap_token(request: Request = None):
    # if not request.headers.get("X-Requested-With"):
    #     raise HTTPException(status_code=400, detail="Incorrect headers")

    # TODO: use for extra client checking?
    # google_client_type = request.headers.get("X-Google-OAuth2-Type")
    print('swap token')
    try:
        body_bytes = await request.body()
        auth_code = jsonable_encoder(body_bytes)

        credentials = client.credentials_from_clientsecrets_and_code(
            GOOGLE_CLIENT_SECRETS_JSON, ["profile", "email"], auth_code
        )

        http_auth = credentials.authorize(httplib2.Http())
        print('http auth:', http_auth)
        print('credentials id:', credentials.id_token)
        google_user_id = credentials.id_token["sub"]

        print("credentials refresh token:", credentials.refresh_token)

    except Exception as E:
        print(E)
        raise HTTPException(status_code=400, detail="Unable to validate social login")

    authenticated_user = await get_current_active_user(google_user_id)

    print("id token:", credentials.id_token)
    print("sub:", credentials.id_token["sub"])
    print("email:", credentials.id_token["email"])
    print("name:", credentials.id_token.get("name", None))
    print("picture:", credentials.id_token.get("picture", None))
    print("given_name:", credentials.id_token.get("given_name", None))
    print("family_name:", credentials.id_token.get("family_name", None))

    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect email address")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={"sub": authenticated_user.ext_id,
              "username": authenticated_user.username,
              },
        expires_delta=access_token_expires
    )

    token = jsonable_encoder(access_token)

    response = JSONResponse({"access_token": token, "token_type": "bearer",               "alg": ALGORITHM,
              "typ": "JWT"})

    print({"token": token,
           "token_type": "bearer",
           "alg": ALGORITHM,
           "typ": "JWT"})

    return response


@security_router.get(f"{ERROR_ROUTE}", tags=["security"])
async def login_error():
    return "Something went wrong logging in!"


@security_router.get(f"{SUCCESS_ROUTE}", response_model=UserDBModel)
async def read_users_me(current_user: UserDBModel = Depends(get_yoba_active_user)):
    print('Read users')
    print('current user')
    print(current_user)
    return current_user
