from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.database import Base
from datetime import datetime

class StoricoPredizioni(Base): 
    __tablename__ = "storico_predizioni"

    id = Column(Integer, primary_key= True, index= True)
    temperatura = Column(Float)
    vibrazioni = Column(Float)
    probabilita_guasto = Column(Float)
    azione_suggerita = Column(String)


class UtenteRegistrato(Base) : 
    __tablename__ = "utenti registrati"

    id = Column(Integer, primary_key=True, index= True)
    email = Column(String, unique= True, index= True)
    password_criptata = Column(String)