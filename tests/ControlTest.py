#----------------------------------------------------
#Exemple de test pour EduRisk
#Groupe N03
#1-28.12.2025
#
#Auteur Daniel Nissille
#Permet de simuler un exemple de tst tout simple en python
#Le résultat est sauvé dans un fichier.csv à la suite des colonnes déjà entrée.
#J'ai utilisé l'aide de ChatGPT pour la partie sauvegarde en csv
#----------------------------------------------------

import time
import csv
import os

#-----------------------------
#PARAMÈTRES
#-----------------------------
CSV_FILE="resultats_qcm.csv"

questions=[
    {
        "question": "Quelle option représente le plus grand risque ?",
        "choices": ["1 chance sur 10", "10 chances sur 100", "1 chance sur 100"],
        "correct": 0
    },
    {
        "question": "Quel événement est le plus probable ?",
        "choices": ["1%", "5%", "10%"],
        "correct": 2
    },
    {
        "question": "Une balle et une batte coûtent 1.10 la batte coûte 1 franc de plus que la balle, combien coûte la balle ?",
        "choices": ["10 centimes", "5 centimes", "impossible de le savoir"],
        "correct": 1
    },
    {
        "question": "Selon l'étude de 2019 quel groupe prend le plus de risque",
        "choices": ["HES", "UNIGE", "Kif-Kif"],
        "correct": 1
    },
    {
        "question": "Une super réduction de 40 pourcent sur déjà 40% vous fait une réduction de ",
        "choices": ["0.80%", "0.64%", "50%"],
        "correct": 0
    }
]

#-----------------------------
#FONCTION QCM
#-----------------------------
def run_qcm():
    responses=[]
    start_time=time.time()

    print("\nDébut du test\n")

    for i, q in enumerate(questions, start=1):
        print(f"Q{i}. {q['question']}")
        for idx, choice in enumerate(q["choices"], start=1):
            print(f"  {idx}. {choice}")

        while True:
            try:
                answer=int(input("Votre choix : "))
                if 1 <= answer <= len(q["choices"]):
                    responses.append(answer)
                    break
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Veuillez entrer un nombre.")

    total_time=round(time.time() - start_time, 2)
    return responses, total_time

#-----------------------------
# SAUVEGARDE CSV une ligne = une personne
#-----------------------------
def save_results(participant_id, edurisk, responses, total_time):
    file_exists = os.path.exists(CSV_FILE)

    headers=["participant_id", "edurisk"]
    headers+=[f"Q{i}" for i in range(1, len(responses) + 1)]
    headers.append("temps_total_sec")

    row=[participant_id, "True" if edurisk else "False"]
    row+=responses
    row.append(total_time)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer=csv.writer(f)

        if not file_exists:
            writer.writerow(headers)

        writer.writerow(row)

if __name__ == "__main__":
    print("=== Test de Risk Literacy ===")

    participant_id=input("ID participant : ")
    edurisk=input("Condition test effectué avec Edurisk ? (True / False) : ").strip().lower() == "true"

    responses, total_time = run_qcm()
    save_results(participant_id, edurisk, responses, total_time)

    print(f"\nTest terminé en {total_time} secondes.")
    print("Résultats sauvegardés.")