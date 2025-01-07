import pandas as pd
from datetime import datetime

def get_teacher_list(file_path):
    """Récupère la liste des enseignants uniques du fichier"""
    df = pd.read_csv(file_path)
    # Récupère tous les enseignants uniques et les trie
    teachers = sorted(df['Intervenant'].dropna().unique())
    return [t.strip() for t in teachers if t.strip()]  # Enlève les espaces et les entrées vides

def display_teacher_menu(teachers):
    """Affiche le menu de sélection des enseignants"""
    print("\n=== Menu de sélection des enseignants ===")
    for i, teacher in enumerate(teachers, 1):
        print(f"{i}. {teacher}")
    print("0. Quitter")
    
    while True:
        try:
            choice = int(input("\nEntrez le numéro de l'enseignant (0 pour quitter) : "))
            if 0 <= choice <= len(teachers):
                return choice
            print("Choix invalide. Veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def determine_modality(group):
    """Détermine la modalité en fonction du groupe"""
    if pd.isna(group):
        return 'TD'
        
    group = str(group).upper().strip()
    
    if group == "1A":
        return 'CM'
    elif "TP" in group:
        return 'TP'
    else:
        return 'TD'

def process_teaching_hours(file_path, teacher_name):
    df = pd.read_csv(file_path)
    df = df[df['Intervenant'].str.contains(teacher_name, case=False, na=False)]
    
    hours = {'CM': 0, 'TD': 0, 'TP': 0}
    modules_by_modality = {'CM': set(), 'TD': set(), 'TP': set()}
    
    for _, row in df.iterrows():
        start = datetime.strptime(row['HStart'], '%H:%M:%S')
        end = datetime.strptime(row['HEnd'], '%H:%M:%S')
        duration = (end - start).total_seconds() / 3600
        
        modalite = determine_modality(row['Groupe'])
        hours[modalite] += duration
        modules_by_modality[modalite].add(row['Summary'].strip())
    
    equivalent_td = hours['CM'] * 1.5 + hours['TD'] + hours['TP'] * 0.66
    
    return hours, equivalent_td, modules_by_modality

def display_service(teacher_name, file_path):
    hours, equivalent_td, modules_by_modality = process_teaching_hours(file_path, teacher_name)
    
    print("\n" + "="*50)
    print(f"Fiche de service pour {teacher_name}")
    print("="*50)
    
    print("\nModules par modalité:")
    for modalite, modules in modules_by_modality.items():
        if modules:
            print(f"\n{modalite}:")
            for module in modules:
                print(f"  - {module}")
    
    print("\nRépartition des heures:")
    print(f"  CM: {hours['CM']:.2f}h")
    print(f"  TD: {hours['TD']:.2f}h")
    print(f"  TP: {hours['TP']:.2f}h")
    print(f"\nTotal équivalent TD: {equivalent_td:.2f}h")
    print("="*50)

def main():
    file_path = 'calendar1912.csv'
    
    while True:
        # Récupère la liste des enseignants
        teachers = get_teacher_list(file_path)
        
        # Affiche le menu et obtient le choix
        choice = display_teacher_menu(teachers)
        
        # Si l'utilisateur choisit 0, quitte le programme
        if choice == 0:
            print("\nAu revoir!")
            break
        
        # Affiche la fiche de service pour l'enseignant choisi
        teacher_name = teachers[choice - 1]
        display_service(teacher_name, file_path)
        
        # Demande si l'utilisateur veut continuer
        continue_choice = input("\nVoulez-vous consulter un autre enseignant? (o/n): ")
        if continue_choice.lower() != '0' or continue_choice.lower() == 'n':
            print("\nAu revoir!")
            break

if __name__ == "__main__":
    main()