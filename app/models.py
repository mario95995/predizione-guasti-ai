from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.database import base
from datetime import datetime

class StoricoPredizioni(base): 
    __tablename__ = "storico_predizioni"

    id = Column(Integer, primary_key= True, index= True)
    temperatura = Column(Float)
    vibrazioni = Column(Float)
    probabilita_guasto = Column(Float)
    azione_suggerita = Column(String)


class UtenteRegistrato(base) : 
    __tablename__ = "utenti registrati"

    id = Column(Integer, primary_key=True, index= True)
    email = Column(String, unique= True, index= True)
    password_criptata = Column(String)