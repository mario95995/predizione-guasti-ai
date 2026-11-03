import csv
import random

def crea_dataset():
    colonne = ['temperatura', 'vibrazioni', 'guasto']

    # Creiamo il file CSV
    with open('macchinari_dataset.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(colonne)
        
        # Generiamo 1000 record simulati
        for _ in range(1000):
            # 80% dei casi: Macchinario Operativo (Guasto = 0)
            if random.random() > 0.2:
                # Valori normali di esercizio
                temp = round(random.uniform(30.0, 70.0), 1)
                vib = round(random.uniform(1.0, 10.0), 1)
                guasto = 0
            
            # 20% dei casi: Macchinario in Anomalia/Guasto (Guasto = 1)
            else:
                # Valori anomali
                temp = round(random.uniform(75.0, 130.0), 1)
                vib = round(random.uniform(12.0, 45.0), 1)
                guasto = 1
                
            writer.writerow([temp, vib, guasto])

if __name__ == "__main__":
    crea_dataset()
    print("File 'macchinari_dataset.csv' generato con successo! (1000 record)")