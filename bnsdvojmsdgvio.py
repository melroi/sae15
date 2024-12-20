import pandas as pd
from datetime import datetime

# Fonction pour lire et nettoyer le fichier CSV
def read_csv(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    # Nettoyage des espaces dans les colonnes
    df['Summary'] = df['Summary'].str.strip()
    df['Intervenant'] = df['Intervenant'].str.strip()
    return df

# Fonction pour filtrer les données par enseignant
def filter_by_teacher(df, teacher_name):
    return df[df['Intervenant'].str.contains(teacher_name, case=False, na=False)]

# Fonction pour attribuer les modalités (à adapter si nécessaire)
def assign_modalities(df):
    # Ajoutez une colonne "Modalité" basée sur un mapping manuel ou des règles
    df['Modalité'] = 'Autre'  # Par défaut
    df.loc[df['Summary'].str.contains('Prog1|Archi-Rés1|Init-Rés1', case=False), 'Modalité'] = 'TD'
    df.loc[df['Summary'].str.contains('Anglais1|SAE1', case=False), 'Modalité'] = 'TP'
    # Ajouter d'autres règles spécifiques si nécessaire
    return df

# Fonction pour calculer les heures
def calculate_hours(df):
    hours_cm = 0
    hours_td = 0
    hours_tp = 0

    for _, row in df.iterrows():
        try:
            start_time = datetime.strptime(row['HStart'], '%H:%M:%S')
            end_time = datetime.strptime(row['HEnd'], '%H:%M:%S')
            duration = (end_time - start_time).total_seconds() / 3600
            
            if row['Modalité'] == 'CM':
                hours_cm += duration
            elif row['Modalité'] == 'TD':
                hours_td += duration
            elif row['Modalité'] == 'TP':
                hours_tp += duration
        except Exception as e:
            print(f"Erreur dans le calcul des heures : {e}")
    
    return hours_cm, hours_td, hours_tp

# Fonction pour convertir les heures en heures équivalentes TD
def convert_to_td(hours_cm, hours_td, hours_tp):
    equivalent_td = hours_cm * 1.5 + hours_td + hours_tp * 0.66
    return equivalent_td

# Fonction pour afficher les résultats
def display_results(teacher_name, hours_cm, hours_td, hours_tp, equivalent_td):
    print(f"Fiche de service pour {teacher_name}")
    print(f"Modules dans lesquels {teacher_name} intervient:")
    print(f"  - CM: {hours_cm:.2f} heures")
    print(f"  - TD: {hours_td:.2f} heures")
    print(f"  - TP: {hours_tp:.2f} heures")
    print(f"Heures équivalentes TD:")
    print(f"  - Total: {equivalent_td:.2f} heures")

def main():
    file_path = 'calendar1912.csv'
    teacher_name = 'FREITAS ANTONIO'  # Nom de l'enseignant à filtrer
    
    df = read_csv(file_path)
    teacher_df = filter_by_teacher(df, teacher_name)
    teacher_df = assign_modalities(teacher_df)  # Attribution des modalités
    hours_cm, hours_td, hours_tp = calculate_hours(teacher_df)
    equivalent_td = convert_to_td(hours_cm, hours_td, hours_tp)
    display_results(teacher_name, hours_cm, hours_td, hours_tp, equivalent_td)

if __name__ == "__main__":
    main()
