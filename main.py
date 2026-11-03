from fastapi import FastAPI, HTTPException, Depends
from app.schemas import DatiSensori
from app.motore_ai import addestra_modello

#importazioni per il database
from sqlalchemy.orm import Session
from app import models
from app.database import engine,get_db

#importazione dei componenti per l'autenticazione sicura
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.security import nascondi_password, verifica_password, crea_token_access
from app.schemas import UtenteRegistrato, Token
import jwt
import os

#addestramento con dati file csv
import joblib


models.Base.metadata.create_all(bind = engine)

app = FastAPI(title="Manutenzione_AI")

# Il server carica istantaneamente la "memoria" già addestrata
modello_ai = joblib.load("modello_industriale.joblib")
#dichiariamo a fastapi dove deve prendere il token 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

#funzione buttafuori
def get_utente_corrente(token : str = Depends(oauth2_scheme)) : 
    try:
        chiave_segreta = os.getenv("JWT_SECRET_KEY")
        #decodifichiamo il codice
        payload = jwt.encode(token, chiave_segreta, algorithms = ["HS256"])
        email_utente = payload("sub")

        if email_utente in None :
            raise HTTPException(status_code= 401, detail= "credenziali non valide")
        return email_utente
    except jwt.PyJWTError : 
        raise HTTPException(status_code= 401, detail= "Token non valido")


#creazione endpoint per la registrazione
@app.post("/api/registrazione")
def registra_utente(utente : UtenteRegistrato, db : Session = Depends(get_db)) : 
    #controlliamo se l'utente è presente nel database
    utente_esistente = db.query(models.UtenteRegistrato).filter(models.UtenteRegistrato.email == utente.email).first()
    if utente_esistente:
        raise HTTPException(status_code=400, detail="Email già registrata")

    #creazione utente usando una password criptata
    nuovo_utente = models.UtenteRegistrato(
        email = utente.email,
        password_criptata = nascondi_password(utente.password)
    )
    db.add(nuovo_utente)
    db.commit()
    db.refresh(nuovo_utente)
    return {"messaggio" : "utente creato con successo"}

#creazione endpoint per il login
@app.post("/api/login", response_model=Token)
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    #ricerca dell'utente nel db
    utente = db.query(models.UtenteRegistrato).filter(models.UtenteRegistrato.email == form_data.username).first()

    #se l'utente non esiste lo blocca
    if not utente or not verifica_password(form_data.password, utente.password_criptata):
        raise HTTPException(status_code=401, detail= "email o password errati")

    #creazione del token
    token_jwt = crea_token_access(dati = {"sub": utente.email})
    return {"access_token": token_jwt, "token_type": "bearer"}





@app.get("/")
async def Manutenzione_Ai():
    return {"sistema": "Manutenzione IOT", "status" : "operativo",}

@app.post("/api/predizione")
async def RiceviDati(prompt : DatiSensori, token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    temperature = prompt.temperatura
    vibration = prompt.vibrazioni

    # calcolo del modello ai
    dati_formattati = [[temperature, vibration]] # fa la lettura di un solo braccio robotico in un preciso istante
    probabilita = modello_ai.predict_proba(dati_formattati)
    
    # CAST A FLOAT: eviterà errori di scrittura nel database SQLite
    prob_guasto = float(probabilita[0][1]) # estraiamo la percentuale di rottura 
    soglia_incertezza = 0.20

    # logica sul danno (USIAMO LE CHIAVI ESATTE PER STREAMLIT)
    if abs(prob_guasto - 0.5) < soglia_incertezza:
        azione = "DUBBIO"
    elif prob_guasto >= 0.5:
        azione = "ALERT"
    else: 
        azione = "OK"

    # salvataggio nel database
    nuova_predizione = models.StoricoPredizioni(
        temperatura = temperature,
        vibrazioni = vibration,
        probabilita_guasto = prob_guasto,
        azione_suggerita = azione
    )
    db.add(nuova_predizione)
    db.commit()
    db.refresh(nuova_predizione)

    # RITORNO AGGIORNATO CON ID
    return {
        "id_record": nuova_predizione.id,
        "probabilita_guasto": prob_guasto,
        "azione": azione
    }

@app.get("/api/storico")
async def ottieni_storico(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Leggiamo gli ultimi 50 record dal database in ordine decrescente (dal più recente)
    storico = db.query(models.StoricoPredizioni).order_by(models.StoricoPredizioni.id.desc()).limit(50).all()
    
    # FastAPI convertirà automaticamente questa lista di oggetti in JSON!
    return storico