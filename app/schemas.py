from pydantic import BaseModel

class DatiSensori(BaseModel):
    temperatura : float
    vibrazioni : float

class UtenteRegistrato(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str