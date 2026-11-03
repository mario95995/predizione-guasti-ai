import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def addestra_modello():
    print("1. Caricamento del dataset...")
    # Leggiamo il "libro di testo" (il CSV)
    df = pd.read_csv('macchinari_dataset.csv')

    # Separiamo le cause (Sensori) dall'effetto (Guasto)
    X = df[['temperatura', 'vibrazioni']] # Le "domande"
    y = df['guasto']                      # Le "risposte giuste"

    print("2. Addestramento del modello AI in corso...")
    # Usiamo una Foresta Casuale (Random Forest), ottima per l'industria
    modello = RandomForestClassifier(n_estimators=100, random_state=42)
    modello.fit(X, y) # Qui avviene la vera e propria magia dell'apprendimento!

    print("3. Salvataggio del cervello...")
    # Congeliamo il modello e lo salviamo in un file
    joblib.dump(modello, 'modello_industriale.joblib')
    
    print("✅ Addestramento completato! File 'modello_industriale.joblib' creato con successo.")

if __name__ == "__main__":
    addestra_modello()