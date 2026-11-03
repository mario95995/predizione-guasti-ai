import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib  # AGGIUNTO: ci serve per salvare il file!

def addestra_modello():
    # 1. Acquisizione e preparazione dei dati
    np.random.seed(42)
    n_campioni = 1000

    # 2. Usiamo variabili normali (non DatiSensori)
    temperatura = np.random.normal(loc=70, scale=10, size=n_campioni)
    vibrazioni = np.random.normal(loc=5, scale=2, size=n_campioni)

    # 3. Definizione del guasto
    guasto = ((temperatura * 0.6 + vibrazioni * 5) > 60).astype(int)

    # 4. Creazione del dataframe
    df = pd.DataFrame(
        {"temperatura": temperatura, "vibrazioni": vibrazioni, "guasto": guasto}
    )
    X = df[["temperatura", "vibrazioni"]] 
    y = df["guasto"]

    # 5. Suddivisione in training set e test set
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 6. Scelta del modello e addestramento
    modello = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    modello.fit(X_train, Y_train)

    y_pred = modello.predict(X_test)
    accuratezza = accuracy_score(Y_test, y_pred)
    print(f"Addestramento completato! Accuratezza: {accuratezza:.2%}")

    # 7. IL PASSAGGIO CHIAVE: Salviamo il modello su disco
    joblib.dump(modello, "modello_industriale.joblib")
    print("Modello salvato con successo nel file 'modello_industriale.joblib'")

if __name__ == "__main__":
    addestra_modello()