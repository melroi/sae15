import pandas as pd
from datetime import datetime

def determine_modality(group):
    """Détermine la modalité en fonction du groupe"""
        
    group = str(group).upper().strip()
    
    # Si le groupe est exactement "1A", c'est un CM
    if group == "1A":
        return 'CM'
    # Si le groupe contient "TP", c'est un TP
    elif "TP" in group:
        return 'TP'
    # Si le groupe contient "TD", ou dans les autres cas, c'est un TD
    else:
        return 'TD'

def process_teaching_hours(file_path, teacher_name):

    df = pd.read_csv(file_path)
    df = df[df['Intervenant'].str.contains(teacher_name, case=False, na=False)]
    
    # Initialisation des compteurs
    hours = {'CM': 0, 'TD': 0, 'TP': 0}
    
    # Dictionnaire pour stocker les modules par modalité
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
    
    print(f"\nFiche de service pour {teacher_name}")
    
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

def main():
    file_path = 'calendar1912.csv'
    teacher_name = input("Nom de l'intervenant: ")
    display_service(teacher_name, file_path)

if __name__ == "__main__":
    main()