⚙️ Utilizzo (Come avviare l'intero sistema)

Per simulare l'ambiente di produzione, avvia i vari componenti nel seguente ordine:

1. Addestra il Modello AI (Fase di Training)
Esegui questo script una sola volta per generare il "cervello" dell'AI (modello_industriale.joblib):

python app/motore_ai.py


2. Avvia il Backend FastAPI (Terminal 1)
Il server girerà all'indirizzo http://localhost:8000:

uvicorn main:app --reload


3. Avvia la Dashboard Streamlit (Terminal 2)
Apri una nuova scheda del terminale e lancia la dashboard (si aprirà automaticamente nel browser all'indirizzo http://localhost:8501):

streamlit run dashboard.py


📊 Regole di Logica Industriale

Il modello stabilisce lo stato del macchinario in base alla formula:
(Temperatura * 0.6 + Vibrazioni * 5) > 60

OK: Nessun intervento richiesto.

DUBBIO: L'AI rileva un'anomalia ma richiede supervisione umana.

ALERT: Rilevata alta probabilità di guasto, arresto immediato richiesto.