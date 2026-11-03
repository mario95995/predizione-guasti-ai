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

    #st.subheader("Invia Dati Sensori")
    # Form per la predizione
    #col1, col2 = st.columns(2)
    #with col1:
     #   temperatura = st.number_input("Temperatura (°C)", min_value=0.0, max_value=150.0, value=60.0)
    #with col2:
     #   vibrazioni = st.number_input("Vibrazioni (mm/s)", min_value=0.0, max_value=50.0, value=5.0)
    st.subheader("📊 Dati Sensori dal Dataset (CSV)")
    try:
        # 1. Leggiamo il CSV
        df_sensori = pd.read_csv("macchinari_dataset.csv")
        
        # 2. Mostriamo tutti i dati in una tabella
        st.dataframe(df_sensori, use_container_width=True)
        
        # 3. Grafico visivo
        st.subheader("📈 Andamento Temperature e Vibrazioni")
        st.line_chart(df_sensori[["temperatura", "vibrazioni"]])
        
        # 4. Prepariamo il terreno per la nuova analisi AI di gruppo
        st.markdown("---")
        if st.button("🧠 Avvia Analisi AI su tutto il dataset"):
            st.info("Qui a breve collegheremo il backend per far analizzare all'AI tutte queste righe!")
            
    except FileNotFoundError:
        st.error("⚠️ File 'macchinari_dataset.csv' non trovato nella cartella.")

    # if st.button("Analizza Macchinario"):
    #     # Prepariamo i dati secondo lo schema Pydantic
    #     payload = {"temperatura": temperatura, "vibrazioni": vibrazioni}
        
    #     # Inseriamo il token nell'header di autorizzazione
    #     headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        
    #     risposta = requests.post("http://127.0.0.1:8000/api/predizione", json=payload, headers=headers)
        
    #     if risposta.status_code == 200:
    #         dati_ricevuti = risposta.json()
    #         azione = dati_ricevuti.get("azione")
    #         prob = dati_ricevuti.get("probabilita_guasto")
            
    #         # Formattazione visiva del risultato corretta (tutto su una riga)
    #         if azione == "OK":
    #             st.success(f"Stato: {azione} - Macchinario operativo (Probabilità guasto: {prob:.1%})")
    #         elif azione == "DUBBIO":
    #             st.warning(f"Stato: {azione} - Richiesta ispezione visiva (Probabilità guasto: {prob:.1%})")
    #         else:
    #             st.error(f"Stato: {azione} - FERMARE IL MACCHINARIO! (Probabilità guasto: {prob:.1%})")
                
    #         st.caption(f"Record salvato nel DB con ID: {dati_ricevuti.get('id_record')}")
            
    #     elif risposta.status_code == 401:
    #         st.error("Token scaduto o non valido. Fai il logout e accedi di nuovo.")
    #     else:
    #         st.error("Errore durante l'elaborazione dei dati.")

    # 4. IL NUOVO PAYLOAD AUTOMATICO
        st.markdown("---")
        st.subheader("🤖 Simulazione Predizione in Tempo Reale")
        st.write("Pesca una lettura dei sensori dal CSV e inviala all'Intelligenza Artificiale.")

        if st.button("Avvia Lettura Sensore e Analisi AI"):
            # 1. Peschiamo una riga a caso dal nostro DataFrame (simula la lettura in tempo reale)
            riga_casuale = df_sensori.sample(n=1).iloc[0]
            
            # 2. ECCO IL PAYLOAD! Usiamo i dati del CSV invece degli input manuali
            payload = {
                "temperatura": float(riga_casuale["temperatura"]),
                "vibrazioni": float(riga_casuale["vibrazioni"])
            }
            
            # Mostriamo a schermo cosa stiamo inviando
            st.info(f"📡 Dati inviati all'AI -> Temperatura: {payload['temperatura']} °C | Vibrazioni: {payload['vibrazioni']} mm/s")
            
            # 3. Chiamata all'API (esattamente come facevi prima!)
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            
            # Assicurati che l'URL sia quello giusto del tuo backend
            risposta = requests.post("http://127.0.0.1:8000/api/predizione", json=payload, headers=headers)
            
            if risposta.status_code == 200:
                risultato = risposta.json()
                azione = risultato["azione"]
                prob = risultato["probabilita_guasto"] * 100
                
                if azione == "OK":
                    st.success(f"✅ STATO: {azione} (Rischio guasto: {prob:.1f}%)")
                elif azione == "DUBBIO":
                    st.warning(f"⚠️ STATO: {azione} (Rischio guasto: {prob:.1f}%)")
                else:
                    st.error(f"🚨 STATO: {azione} (Rischio guasto: {prob:.1f}%)")
            else:
                st.error("Errore di comunicazione col server AI.")

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
                # Creiamo una colonna testuale solo per rendere il grafico più leggibile
                df_grafico = df_sensori.copy()
                df_grafico["Stato Macchinario"] = df_grafico["guasto"].apply(lambda x: "Guasto 🔴" if x == 1 else "OK 🟢")

                # Disegniamo il grafico a dispersione
                st.scatter_chart(
                    data=df_grafico,
                    x="temperatura",
                    y="vibrazioni",
                    color="Stato Macchinario"
                )
                
            else:
                st.info("Nessun dato presente nello storico. Fai prima qualche predizione!")
        else:
            st.error("Impossibile caricare lo storico. Verifica la connessione.")