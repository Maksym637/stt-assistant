import requests

from authlib.jose import JsonWebToken
from authlib.jose.errors import JoseError

from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer

from schemas.auth import Auth0Payload

from config import api_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
jwt = JsonWebToken(["RS256"])


def get_jwk():
    response = requests.get(
        f"https://{api_settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    )
    return response.json()


def verify_jwt_token(token: str, audience: str, approved_claim: str):
    try:

        jwks = get_jwk()
        claims = jwt.decode(token, jwks)
        claims.validate()

        if audience not in claims.get("aud", []):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid audience"
            )

        if not claims.get(approved_claim, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Account not approved"
            )

        return claims

    except JoseError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_current_account(token: str = Security(oauth2_scheme)):
    audience = api_settings.AUTH0_AUDIENCE

    approved_claim = f"{audience}/approved"
    claims = verify_jwt_token(token, audience, approved_claim)

    return Auth0Payload(sub=claims["sub"], email=claims.get("email", ""))
