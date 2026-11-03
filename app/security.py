from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

#configurazione jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#funzioni di sicurezza 
def nascondi_password(password_in_chiaro : str) -> str : 
    return pwd_context.hash(password_in_chiaro)

def verifica_password(password_in_chiaro :str, password_nel_db : str) -> bool : 
    return pwd_context.verify(password_in_chiaro,password_nel_db)


def crea_token_access(dati : dict) -> str : 
    dati_da_codificare = dati.copy()
    scadenza = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dati_da_codificare.update({"exp" : scadenza})

    token_codificato = jwt.encode(dati_da_codificare, SECRET_KEY, ALGORITHM)
    return token_codificato