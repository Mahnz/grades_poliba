import json
import os
from datetime import datetime

FILE_JSON = "exams.json"


def load_json():
    """ Load data from JSON file """
    if os.path.exists(FILE_JSON):
        with open(FILE_JSON, "r") as file:
            return json.load(file)
    return {"exams": [], "alpha": 0, "lodi": 0, "anni_fuori_corso": 0}


def save_json(dati):
    """ Save data to JSON file """
    dati["exams"] = sorted(dati["exams"], key=lambda x: datetime.strptime(x["date"], "%d-%m-%Y")
    if x["date"] else datetime.max)

    with open(FILE_JSON, "w") as file:
        json.dump(dati, file, indent=4)


def reset_exams():
    """ Reset grades and dates for each exam """
    confirm = input("[!] Sei sicuro di voler resettare tutti gli esami? (s/n): ")
    if confirm.lower() not in ["s", "si", "y", "yes"]:
        dati = load_json()

        for e in dati["exams"]:
            e["grade"] = 0
            e["date"] = None

        save_json(dati)
    else:
        print("[!] Reset annullato.")


def add_exam():
    """ Add a new exam to the list """
    data = load_json()
    to_do = [e for e in data["exams"] if e["grade"] == 0]

    if not to_do:
        print("[!] Non ci sono esami disponibili per essere aggiunti.")
        return

    print("[*] Esami da aggiungere:")
    for i, esame in enumerate(to_do, 1):
        print(f"     {i}) {esame["name"]} ({esame["CFU"]} CFU)")
    print()

    choice = int(input("[+] Seleziona l'esame da aggiornare (numero): ")) - 1
    if choice < 0 or choice >= len(to_do):
        print("[!] Scelta non valida.")
        return

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

    print(f"[*] Esame selezionato: {to_do[choice]["name"].upper()} - CFU {to_do[choice]["CFU"]}")
    while True:
        grade = input(f"    Voto: ").strip().upper()
        if grade == "30L":
            grade = 31
            break
        else:
            grade = int(grade)
            if 18 <= grade <= 31:
                break
            else:
                print("     > Il voto deve essere compreso tra 18 e 31.\n")

    while True:
        date = input("    Data (DD-MM-YYYY): ")
        if date:
            try:
                datetime.strptime(date, "%d-%m-%Y")
                break
            except ValueError:
                print("     > Data non valida. Riprova.\n")
        else:
            break

    data["exams"][data["exams"].index(to_do[choice])]["grade"] = grade
    data["exams"][data["exams"].index(to_do[choice])]["date"] = date

    save_json(data)

    print(f"[*] Esame aggiornato: {to_do[choice]['name']} - Voto {grade}")


def remove_exam():
    """ Remove an exam from the list """
    dati = load_json()
    done = [e for e in dati["exams"] if e["grade"] > 0]

    print("[*] Esami disponibili:")
    for i, esame in enumerate(done, 1):
        print(f"     {i}) {esame['name']} - Voto {esame['voto']} - CFU {esame['CFU']}")
    print()

    s = int(input("[+] Seleziona l'esame da rimuovere (numero): ")) - 1

    if s < 0 or s >= len(dati["exams"]):
        print("[!] Scelta non valida.")
        return
    else:
        dati["exams"][s]["grade"] = 0
        dati["exams"][s]["date"] = None
        save_json(dati)


def weighted_average(exams, cfu_off=0):
    """ Compute the weighted average of the exams """
    exams = sorted(exams, key=lambda x: x["grade"])
    exams = [e for e in exams if e["grade"] > 0]
    filtered = []

    for e in exams:
        e["grade"] = 30 if e["grade"] == 31 else e["grade"]

        if cfu_off > 0:
            if e["CFU"] <= cfu_off:
                cfu_off -= e["CFU"]
                continue
            else:
                filtered.append({"grade": e["grade"], "CFU": e["CFU"] - cfu_off})
                cfu_off = 0
        else:
            filtered.append(e)

    avg = sum(e["grade"] * e["CFU"] for e in exams) / sum(e["CFU"] for e in exams) if exams else 0
    avg_filtered = sum(e["grade"] * e["CFU"] for e in filtered) / sum(e["CFU"] for e in filtered) if filtered else 0

    return avg, avg_filtered


def voto_partenza(data=None):
    data = load_json() if data is None else data
    avg, avg_filtered = weighted_average(data["exams"], int(data.get("cfu_off")))
    avg_110 = (avg * 110) / 30
    avg_filtered_110 = (avg_filtered * 110) / 30

    alpha = int(data.get("alpha"))

    lodi = data["exams"].count(31)
    gamma = 0.01 if lodi >= 2 else 0.005 if lodi == 1 else 0.0

    if data["anni_fuori_corso"] > 1:
        delta = 0
    elif data["anni_fuori_corso"] == 1:
        delta = 0.005
    else:
        delta = 0.01

    k = 1 + alpha + gamma + delta
    partenza_110 = avg_110 * k
    partenza_filtered_110 = avg_filtered_110 * k

    print(f"[*] Parametri:\n"
          f"     > alpha = {alpha}  |  gamma = {gamma}  |  delta = {delta}\n"
          f"     > Media Ponderata: {avg:.2f} --> {avg_110:.2f}\n"
          f"     > Media Ponderata (FILTRATO): {avg_filtered:.2f} --> {avg_filtered_110:.2f}\n")

    print(f"[*] Voto di partenza: {partenza_110:.2f}")
    print(f"[*] Voto di partenza (FILTRATO): {partenza_filtered_110:.2f}")


def simulate_exam():
    """ Simulate adding an exam without saving it """
    data = load_json()

    grade = int(input("[+] Inserisci voto esame: "))
    cfu = int(input("[+] Inserisci CFU esame: "))
    simulated_data = {
        **data, "exams": data["exams"] + [{"name": "Simulazione", "grade": grade, "CFU": cfu, "date": None}]
    }

    voto_partenza(simulated_data)


if __name__ == "__main__":
    while True:
        if not os.path.exists(FILE_JSON):
            print("[!] File JSON non trovato. Creazione di 'exams.json' dal template.")
            with open("template_exams.json", "r") as file:
                with open(FILE_JSON, "w") as new_file:
                    new_file.write(file.read())


        print("\n- - - - - - - - - - Gestione Voto di Laurea - - - - - - - - - -")
        print("1) Aggiungi esame")
        print("2) Rimuovi esame")
        print("3) Calcolo voto di partenza")
        print("4) Reset esami")
        print("5) Simula un voto")
        print("6) Esci\n")
        s = input("[+] Seleziona un'opzione: ")

        if s == "1":
            print("\n- - - - - - - - - - - - AGGIUNTA ESAME - - - - - - - - - - - -\n")
            add_exam()

        elif s == "2":
            print("\n- - - - - - - - - - - - RIMOZIONE ESAME - - - - - - - - - - - -\n")
            remove_exam()

        elif s == "3":
            print("\n- - - - - - - - - - - - VOTO DI LAUREA - - - - - - - - - - - -\n")
            voto_partenza()
            break

        elif s == "4":
            print("\n- - - - - - - - - - - - RESET LIBRETTO - - - - - - - - - - - -\n")
            reset_exams()
            break

        elif s == "5":
            print("\n- - - - - - - - - - - SIMULAZIONE VOTO - - - - - - - - - - - -\n")
            simulate_exam()
            break

        elif s == "6":
            print("[!] Uscita dal programma.")
            break

        else:
            print("[!] Scelta non valida. Riprova.")
