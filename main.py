from fastapi import FastAPI, HTTPException
from app.schemas import DatiSensori
from app.motore_ai import addestra_modello

app = FastAPI(title="Manutenzione_AI")
modello_ai, accuratezza_modello = addestra_modello()


@app.get("/")
async def Manutenzione_Ai():
    return {"sistema": "Manutenzione IOT", "status" : "operativo", "accuratezza_modello" : accuratezza_modello}

@app.post("/api/predizione")
async def RiceviDati(prompt : DatiSensori):
    temperature = prompt.temperatura
    vibration = prompt.vibrazioni

    dati_formattati = [[temperature, vibration]] # fa la lettura di un solo braccio robotico in un preciso instante
    probabilita = modello_ai.predict_proba(dati_formattati)
    prob_guasto = probabilita[0][1] #estraiamo la percentuale di rottura 
    soglia_incertezza = 0.20

    if abs(prob_guasto - 0.5) < soglia_incertezza :
        azione = "DUBBIO: Richiesto intervento del Business Analyst / Tecnico umano."
    elif prob_guasto >= 0.5:
        azione = "ALERT: Attivare procedura d'emergenza (Manutenzione immediata)."
    else : azione = "OK: Funzionamento regolare del braccio robotico."

    return {
    "probabilita_guasto": prob_guasto,
    "azione": azione
    }

    