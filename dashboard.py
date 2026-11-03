import streamlit as st
import requests
import pandas as pd  # AGGIUNTO: ci serve per manipolare i dati del grafico

# Configurazione della pagina
st.set_page_config(page_title="Dashboard Manutenzione AI", layout="centered")
st.title("⚙️ Pannello di Manutenzione Predittiva")

# 1. Inizializza lo stato della sessione per il token
if 'token' not in st.session_state:
    st.session_state['token'] = None

# --- SEZIONE AUTENTICAZIONE ---
if st.session_state['token'] is None:
    tab_login, tab_registrazione = st.tabs(["🔑 Login", "📝 Nuova Registrazione"])
    
    with tab_login:
        st.subheader("Accesso Operatore")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            dati_login = {"username": email, "password": password}
            try:
                risposta = requests.post("http://127.0.0.1:8000/api/login", data=dati_login)
                if risposta.status_code == 200:
                    st.session_state['token'] = risposta.json().get("access_token")
                    st.rerun()
                else:
                    st.error("Email o password errati. Riprova.")
            except requests.exceptions.ConnectionError:
                st.error("Impossibile connettersi al Backend. Uvicorn è acceso?")

    with tab_registrazione:
        st.subheader("Crea un nuovo account")
        reg_email = st.text_input("Nuova Email", key="reg_email")
        reg_password = st.text_input("Nuova Password", type="password", key="reg_pass")
        
        if st.button("Registrati"):
            payload_reg = {"email": reg_email, "password": reg_password}
            try:
                risposta_reg = requests.post("http://127.0.0.1:8000/api/registrazione", json=payload_reg)
                
                if risposta_reg.status_code == 200:
                    st.success("Operatore registrato con successo! Ora puoi fare il login.")
                elif risposta_reg.status_code == 400:
                    st.error("Email già presente nel sistema. Usa un'altra email.")
                else:
                    st.error("Errore durante la registrazione.")
            except requests.exceptions.ConnectionError:
                st.error("Impossibile connettersi al Backend.")    

# --- SEZIONE DASHBOARD (Visibile solo se loggati) ---
else:
    st.success("Autenticazione completata.")
    if st.button("Logout"):
        st.session_state['token'] = None
        st.rerun()

    st.subheader("Invia Dati Sensori")
    # Form per la predizione
    col1, col2 = st.columns(2)
    with col1:
        temperatura = st.number_input("Temperatura (°C)", min_value=0.0, max_value=150.0, value=60.0)
    with col2:
        vibrazioni = st.number_input("Vibrazioni (mm/s)", min_value=0.0, max_value=50.0, value=5.0)

    if st.button("Analizza Macchinario"):
        # Prepariamo i dati secondo lo schema Pydantic
        payload = {"temperatura": temperatura, "vibrazioni": vibrazioni}
        
        # Inseriamo il token nell'header di autorizzazione
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        
        risposta = requests.post("http://127.0.0.1:8000/api/predizione", json=payload, headers=headers)
        
        if risposta.status_code == 200:
            dati_ricevuti = risposta.json()
            azione = dati_ricevuti.get("azione")
            prob = dati_ricevuti.get("probabilita_guasto")
            
            # Formattazione visiva del risultato corretta (tutto su una riga)
            if azione == "OK":
                st.success(f"Stato: {azione} - Macchinario operativo (Probabilità guasto: {prob:.1%})")
            elif azione == "DUBBIO":
                st.warning(f"Stato: {azione} - Richiesta ispezione visiva (Probabilità guasto: {prob:.1%})")
            else:
                st.error(f"Stato: {azione} - FERMARE IL MACCHINARIO! (Probabilità guasto: {prob:.1%})")
                
            st.caption(f"Record salvato nel DB con ID: {dati_ricevuti.get('id_record')}")
            
        elif risposta.status_code == 401:
            st.error("Token scaduto o non valido. Fai il logout e accedi di nuovo.")
        else:
            st.error("Errore durante l'elaborazione dei dati.")

        # --- SEZIONE STORICO ---
    st.divider() # Traccia una linea orizzontale per separare le sezioni
    st.subheader("📊 Storico Interventi e Predizioni")
    
    if st.button("Carica Storico Dati"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        
        # Facciamo una chiamata GET alla nuova rotta
        risposta_storico = requests.get("http://127.0.0.1:8000/api/storico", headers=headers)
        
        if risposta_storico.status_code == 200:
            dati_storico = risposta_storico.json()
            
            if dati_storico:
                # 1. Convertiamo i dati ricevuti in un DataFrame di Pandas
                df_storico = pd.DataFrame(dati_storico)
                
                # Mostriamo la tabella (come prima)
                st.dataframe(df_storico, use_container_width=True)
                
                # --- NUOVO: GRAFICO VISIVO ---
                st.subheader("📈 Andamento Temperature e Vibrazioni")
                
                # Ordiniamo i dati dall'ID più piccolo (vecchio) al più grande (recente) 
                # per far andare il grafico da sinistra verso destra nel tempo
                df_grafico = df_storico.sort_values(by="id")
                
                # Impostiamo l'ID come asse X del nostro grafico
                df_grafico.set_index("id", inplace=True)
                
                # Disegniamo il grafico a linee usando solo le colonne dei sensori
                st.line_chart(df_grafico[["temperatura", "vibrazioni"]])
                
            else:
                st.info("Nessun dato presente nello storico. Fai prima qualche predizione!")
        else:
            st.error("Impossibile caricare lo storico. Verifica la connessione.")