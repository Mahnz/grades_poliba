#!/usr/bin/env python3
import json
import os
from datetime import datetime

FILE_JSON = "exams.json"
BASE_DATA = {
    "exams": [],
    "fuori_corso": 0,
    "cfu_off": 9,
    "alpha": 0,
}


def load_json():
    """Load data from JSON file"""
    if os.path.exists(FILE_JSON):
        with open(FILE_JSON, "r") as file:
            return json.load(file)


def save_json(data):
    """Save data to JSON file"""
    data["exams"] = sorted(
        data["exams"],
        key=lambda x: (
            datetime.strptime(x["date"], "%d-%m-%Y") if x["date"] else datetime.max
        ),
    )

    with open(FILE_JSON, "w") as file:
        json.dump(data, file, indent=4)


def list_exams(exams):
    for i, e in enumerate(exams, 1):
        print(f'     {i}) {e["name"]} ({e["CFU"]} CFU)')
    print()


def reset_exams(data):
    """Reset grades and dates for each exam"""
    choice = (
        input("[!] Are you sure you want to reset all exams? (y/n): ").strip().lower()
    )
    if choice in ["y", "yes"]:
        for e in data["exams"]:
            e["grade"] = 0
            e["date"] = None

        save_json(data)
        print("    All exams have been reset.")
    else:
        print("[!] Reset cancelled.")


def add_exam(data):
    """Add a new exam to the list"""

    to_do = [e for e in data["exams"] if e["grade"] == 0]

    if to_do:
        print("[*] Exams registered WITH NO GRADE:")
        list_exams(to_do)

        while True:
            try:
                choice = int(
                    input(
                        "[+] Enter the exam index to register it, [0] to add a new exam: "
                    )
                    .strip()
                    .lower()
                )
                if choice < 0 or choice > len(to_do):
                    print("[!] Invalid choice. Try again.")
                    continue
                break
            except ValueError:
                print("[!] Please enter a valid number.")
        print()
    else:
        choice = 0

    if choice == 0:
        name = input("[+] Enter new exam name: ").strip()
        cfu = int(input("[+] Enter exam CFU: "))

        add_grade = input("[+] Do you want to add a grade now? (y/n): ").strip().lower()

        if add_grade in ["y", "yes"]:
            while True:
                grade = input(f"    Grade: ").strip().upper()
                if (grade == "30L") or (grade == "31"):
                    grade = 31
                    break
                else:
                    grade = int(grade)
                    if 18 <= grade <= 31:
                        break
                    else:
                        print("     > Grade must be between 18 and 31.\n")

            while True:
                date = input("    Date (DD-MM-YYYY): ")
                if date:
                    try:
                        datetime.strptime(date, "%d-%m-%Y")
                        break
                    except ValueError:
                        print("     > Invalid date. Try again.\n")
                else:
                    break
        else:
            grade = 0
            date = None

        new_exam = {"name": name, "CFU": cfu, "grade": grade, "date": date}

        data["exams"].append(new_exam)
        save_json(data)

        if grade > 0:
            print(f"[*] Exam added: {name} - Grade {grade}")
        else:
            print(f"[*] Exam added: {name} (no grade yet)")
    else:
        exam = to_do[choice - 1]
        print(f"\n[*] Selected exam: {exam['name'].upper()} - CFU {exam['CFU']}")

        while True:
            grade = input(f"    Grade: ").strip().upper()
            if (grade == "30L") or (grade == "31"):
                grade = 31
                break
            else:
                grade = int(grade)
                if 18 <= grade <= 31:
                    break
                else:
                    print("     > Grade must be between 18 and 31.\n")

        while True:
            date = input("    Date (DD-MM-YYYY): ")
            if date:
                try:
                    datetime.strptime(date, "%d-%m-%Y")
                    break
                except ValueError:
                    print("     > Invalid date. Try again.\n")
            else:
                break

        data["exams"][data["exams"].index(exam)]["grade"] = grade
        data["exams"][data["exams"].index(exam)]["date"] = date

        save_json(data)

        print(f"[*] Exam updated: {exam['name']} - Grade {grade}")


def update_exam(data):
    """Update an existing exam's grade and date"""

    exams = [e for e in data["exams"] if e["grade"] > 0]
    if not exams:
        print("[!] No exams with grades found. Please add an exam first.")
        return

    print("[*] Exams registered:")
    list_exams(exams)

    choice = int(input("[+] Select the exam to update (number): ")) - 1
    if choice < 0 or choice >= len(exams):
        print("[!] Invalid choice.")
        return

    print("\n========= ========= ========= ========= ========= = =\n")

    print(
        f'[*] Selected exam: {exams[choice]["name"].upper()} - CFU {exams[choice]["CFU"]}'
    )
    while True:
        grade = input(f"    Grade: ").strip().upper()
        if (grade == "30L") or (grade == "31"):
            grade = 31
            break
        else:
            grade = int(grade)
            if 18 <= grade <= 31:
                break
            else:
                print("     > Grade must be between 18 and 31.\n")

    while True:
        date = input("    Date (DD-MM-YYYY): ")
        if date:
            try:
                datetime.strptime(date, "%d-%m-%Y")
                break
            except ValueError:
                print("     > Invalid date. Try again.\n")
        else:
            break

    data["exams"][data["exams"].index(exams[choice])]["grade"] = grade
    data["exams"][data["exams"].index(exams[choice])]["date"] = date

    save_json(data)

    print(f"[*] Exam updated: {exams[choice]['name']} - Grade {grade}")


def remove_exam(data):
    """Remove an exam from the list"""

    print("[*] Available exams:")
    list_exams(data["exams"])

    s = int(input("[+] Select the exam to remove (number): ")) - 1

    if s < 0 or s >= len(data["exams"]):
        print("[!] Invalid choice.")
        return
    else:
        data["exams"].pop(s)
        save_json(data)


def weighted_average(exams, cfu_off=0):
    """Compute the weighted average of the exams"""
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

    avg = (
        sum(e["grade"] * e["CFU"] for e in exams) / sum(e["CFU"] for e in exams)
        if exams
        else 0
    )
    avg_filtered = (
        sum(e["grade"] * e["CFU"] for e in filtered) / sum(e["CFU"] for e in filtered)
        if filtered
        else 0
    )

    return avg, avg_filtered


def starting_grade(data):
    """Compute the starting grade based on the exams"""
    if not data["exams"]:
        print("[!] No exams found. Please add exams first.")
        return

    avg, avg_filtered = weighted_average(data["exams"], int(data.get("cfu_off")))
    avg_110 = (avg * 110) / 30
    avg_filtered_110 = (avg_filtered * 110) / 30

    alpha = float(data.get("alpha"))

    lodi = data["exams"].count(31)
    gamma = 0.01 if lodi >= 2 else 0.005 if lodi == 1 else 0.0

    if data["fuori_corso"] > 1:
        delta = 0
    elif data["fuori_corso"] == 1:
        delta = 0.005
    else:
        delta = 0.01

    k = 1 + alpha + gamma + delta
    partenza_110 = avg_110 * k
    partenza_filtered_110 = avg_filtered_110 * k

    print(
        f"[*] Parameters:\n"
        f"     > alpha = {alpha}  |  gamma = {gamma}  |  delta = {delta}\n"
        f"     > Weighted Average: {avg:.2f} --> {avg_110:.2f}\n"
        f"     > Weighted Average (FILTERED): {avg_filtered:.2f} --> {avg_filtered_110:.2f}\n"
    )

    print(f"[*] Starting grade: {partenza_110:.2f}")
    print(f"[*] Starting grade (FILTERED): {partenza_filtered_110:.2f}")


def simulate_exam(data):
    """Simulate adding an exam without saving it"""

    grade = int(input("[+] Enter exam grade: "))
    cfu = int(input("[+] Enter exam CFU: "))
    simulated_data = {
        **data,
        "exams": data["exams"]
        + [{"name": "Simulation", "grade": grade, "CFU": cfu, "date": None}],
    }
    starting_grade(simulated_data)


def modify_parameters(data):
    """Modify the parameters fuori_corso, cfu_off, and alpha"""
    print(f"[*] Current parameters:")
    print(f"     > fuori_corso: {data['fuori_corso']}")
    print(f"     > cfu_off: {data['cfu_off']}")
    print(f"     > alpha: {data['alpha']}")
    print()

    modify = (
        input("[+] Do you want to modify these parameters? (y/n): ").strip().lower()
    )
    if modify not in ["y", "yes"]:
        print("[!] Parameter modification cancelled.")
        return

    print("\n[*] Enter new values (press Enter to keep current value):")

    fuori_corso_input = input(
        f"    fuori_corso (current: {data['fuori_corso']}): "
    ).strip()
    if fuori_corso_input:
        data["fuori_corso"] = int(fuori_corso_input)

    cfu_off_input = input(f"    cfu_off (current: {data['cfu_off']}): ").strip()
    if cfu_off_input:
        data["cfu_off"] = int(cfu_off_input)

    alpha_input = input(f"    alpha (current: {data['alpha']}): ").strip()
    if alpha_input:
        data["alpha"] = float(alpha_input)

    save_json(data)

    print(f"[*] Parameters updated:")
    print(f"     > fuori_corso: {data['fuori_corso']}")
    print(f"     > cfu_off: {data['cfu_off']}")
    print(f"     > alpha: {data['alpha']}")


def list_all_exams(data):
    """List all registered exams in a fashionable way"""
    if not data["exams"]:
        print("[!] No exams registered yet.")
        return

    completed = [e for e in data["exams"] if e["grade"] > 0]
    pending = [e for e in data["exams"] if e["grade"] == 0]

    print(
        f"[*] Total exams: {len(data['exams'])} | Completed: {len(completed)} | Pending: {len(pending)}"
    )

    if completed:
        max_name_width = max(len(exam["name"]) for exam in completed)
        name_width = max(max_name_width + 2, 20)
        total_width = name_width + 25 + 5

        print("\n🎓 COMPLETED EXAMS:")
        print("─" * total_width)
        print(f"{'#':<3} {'Name':<{name_width}} {'CFU':<5} {'Grade':<7} {'Date':<12}")
        print("─" * total_width)

        for i, exam in enumerate(completed, 1):
            grade_display = "30L" if exam["grade"] == 31 else str(exam["grade"])
            date_display = exam["date"] if exam["date"] else "N/A"
            print(
                f"{i:<3} {exam['name']:<{name_width}} {exam['CFU']:<5} {grade_display:<7} {date_display:<12}"
            )

    if pending:
        max_name_width = max(len(exam["name"]) for exam in pending)
        name_width = max(max_name_width + 2, 20)
        total_width = name_width + 10

        if not completed:
            print("=" * total_width)

        print(f"\n📝 PENDING EXAMS:")
        print("─" * total_width)
        print(f"{'#':<3} {'Name':<{name_width}} {'CFU':<5}")
        print("─" * total_width)

        for i, exam in enumerate(pending, 1):
            print(f"{i:<3} {exam['name']:<{name_width}} {exam['CFU']:<5}")

    if completed:
        total_cfu = sum(e["CFU"] for e in completed)
        avg, _ = weighted_average(data["exams"])
        print(f"\n📊 SUMMARY: {total_cfu} CFU completed | Average: {avg:.2f}")


if __name__ == "__main__":
    print("\n════════════════════════ GRADE MANAGER ════════════════════════")

    while True:
        if not os.path.exists(FILE_JSON):
            print(
                "[!] JSON file not found. Creating 'exams.json' with default structure.\n"
            )
            # Create the base JSON structure
            with open(FILE_JSON, "w") as file:
                json.dump(BASE_DATA, file, indent=4)

        data = load_json()

        print("1) Add an exam grade")
        print("2) Update an exam grade")
        print("3) Remove exam")
        print("4) Compute your starting grade")
        print("5) Reset exams")
        print("6) Simulate a grade")
        print("7) Modify parameters")
        print("8) List all exams")
        print("[0] Exit\n")
        s = input("[+] Select an option: ")

        if s == "1":
            print("\n══════════════════════ ADD EXAM ══════════════════════\n")
            add_exam(data)

        elif s == "2":
            print("\n══════════════════════ EDIT EXAM ══════════════════════\n")
            update_exam(data)

        elif s == "3":
            print("\n═════════════════════ REMOVE EXAM ═════════════════════\n")
            remove_exam(data)

        elif s == "4":
            print("\n════════════════ STARTING DEGREE GRADE ════════════════\n")
            starting_grade(data)
            break

        elif s == "5":
            print("\n══════════════════ RESET TRANSCRIPT ══════════════════\n")
            reset_exams(data)
            break

        elif s == "6":
            print("\n══════════════════ GRADE SIMULATION ══════════════════\n")
            simulate_exam(data)
            break

        elif s == "7":
            print("\n══════════════════ MODIFY PARAMETERS ══════════════════\n")
            modify_parameters(data)

        elif s == "8":
            print("\n════════════════════ ALL EXAMS ════════════════════\n")
            list_all_exams(data)

        elif s == "0":
            print("[!] Exiting program.")
            break

        else:
            print("[!] Invalid choice. Try again.")

        print("\n═══════════════════ ═══════════════════════ ═══════════════════\n")
