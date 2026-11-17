"""Segurança demonstrativa para o MVP.

Em produção, mova o segredo para variável de ambiente/secret manager, use TLS,
rotacione chaves e substitua o token didático por sessões curtas com refresh token.
"""
from datetime import datetime, timedelta, timezone
import os
from argon2 import PasswordHasher
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

_password_hasher = PasswordHasher()
_secret_key = os.getenv("APASFA_SECRET_KEY", "dev-only-change-me")
_algorithm = "HS256"
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Usuário fictício: a senha real nunca aparece no repositório.
_demo_email = os.getenv("APASFA_DEMO_EMAIL", "cuidados@apasfa.org.br")
_demo_password_hash = _password_hasher.hash(os.getenv("APASFA_DEMO_PASSWORD", "troque-esta-senha"))

def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return _password_hasher.verify(password_hash, plain_password)
    except Exception:
        return False

def create_access_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode({"sub": subject, "exp": expires}, _secret_key, algorithm=_algorithm)

def authenticate_demo_user(email: str, password: str) -> bool:
    return email == _demo_email and verify_password(password, _demo_password_hash)

def get_current_user(token: str = Depends(_oauth2_scheme)) -> str:
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, _secret_key, algorithms=[_algorithm])
        subject = payload.get("sub")
        if not subject:
            raise credentials_error
        return str(subject)
    except JWTError as exc:
        raise credentials_error from exc
