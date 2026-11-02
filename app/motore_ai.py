from app.schemas import DatiSensori
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


prompt = DatiSensori

def addestra_modello():
    #1 acquisizione e preparazione dei dati
    np.random.seed(42)
    n_campioni = 1000

    #2 simulazioni distribuzioni gaussiane per temperatura e vibrazioni 
    prompt.temperatura = np.random.normal(loc=70, scale=10, size= n_campioni)
    prompt.vibrazioni = np.random.normal(loc=5, scale=2, size= n_campioni)

    #3 definizione del guasto (1 = guasto, 0 = regolare), se con la definizione ponderata supera la soglia dei 60 il danno e critico
    guasto = ((prompt.temperatura * 0.6 + prompt.vibrazioni * 5) > 60).astype(int)

    #4 creazione del dataframe, definizione feature x e target y
    df = pd.DataFrame(
        {"temperatura" : prompt.temperatura, "vibrazioni" : prompt.vibrazioni, "guasto" : guasto}
    )
    X = df[["temperatura", "vibrazioni"]] #matrice
    y = df["guasto"]

    #suddivisione in training set (70%), e test set(30%)
    X_train, X_test, Y_train, Y_test= train_test_split(
        X, y, test_size= 0.3 , random_state= 42
    )

    #Scelta del modello e addestramento
    modello = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    modello.fit(X_train, Y_train)

    y_pred = modello.predict(X_test)
    accuratezza  = accuracy_score(Y_test, y_pred)

    return modello, accuratezza