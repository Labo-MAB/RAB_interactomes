import pandas as pd

# Input and output file
MAXQUANT = "data/proteinGroups.txt"
FILTERED_MAXQUANT = "data/proteinGroups_filtered.tsv"
BAIT = "data/bait.txt" # Manually created file
INTERACTION = "data/interaction.txt"
PREY = "data/prey.txt"

# Étape 1 : filtrer le proteinGroups.txt
df = pd.read_csv(MAXQUANT, sep='\t')

filtered_df = df[
    (df['Potential contaminant'] != '+') &
    (df['Reverse'] != '+') &
    (df['Only identified by site'] != '+')
]

filtered_df.to_csv(FILTERED_MAXQUANT, sep='\t', index=False)
print(f"Fichier filtré sauvegardé sous : {FILTERED_MAXQUANT}")

# Étape 2 : charger le fichier filtré
filtered_df = pd.read_csv(FILTERED_MAXQUANT, sep='\t')

# Étape 3 : sélectionner les colonnes Majority protein IDs + MS/MS count
count_cols = [col for col in filtered_df.columns if col.startswith('MS/MS count ')]
df_counts = filtered_df[['Majority protein IDs'] + count_cols]

# Étape 4 : lire bait.txt
bait_df = pd.read_csv(BAIT, sep='\t', header=None, names=['IP name', 'bait', 'T/C'])

# Étape 5 : transformer le tableau large en tableau long
df_long = df_counts.melt(id_vars='Majority protein IDs', value_vars=count_cols,
                         var_name='IP name', value_name='count')

# Étape 6 : nettoyer les noms d'IP name (enlever "MS/MS count ")
df_long['IP name'] = df_long['IP name'].str.replace('MS/MS count ', '', regex=False)

# Étape 7 : extraire premier identifiant si Majority protein IDs contient des ;
df_long['prey'] = df_long['Majority protein IDs'].str.split(';').str[0]

# Étape 8 : ajouter la colonne bait par correspondance
df_long = df_long.merge(bait_df[['IP name', 'bait']], on='IP name', how='left')

# Étape 9 : supprimer les lignes avec count == 0 ou NaN
df_long = df_long[df_long['count'].fillna(0) != 0]

# Étape 10 : sauvegarder le fichier interaction.txt
df_long[['IP name', 'bait', 'prey', 'count']].to_csv(INTERACTION, sep='\t', header=False, index=False)

print(f"interaction.txt généré avec succès sous : {INTERACTION}")

# Étape 11 : générer prey.txt
prey_df = filtered_df[['Majority protein IDs', 'Sequence length', 'Gene names']].drop_duplicates()

# Renommer les colonnes
prey_df = prey_df.rename(columns={'Majority protein IDs': 'prey', 'Sequence length': 'length', 'Gene names': 'gene'})

# Extraire seulement le premier identifiant si Majority protein IDs contient des ;
prey_df['prey'] = prey_df['prey'].str.split(';').str[0]

# Extraire seulement le premier gene name si besoin
prey_df['gene'] = prey_df['gene'].str.split(';').str[0]

# Remplacer NaN gene par même valeur que prey si absent
prey_df['gene'] = prey_df['gene'].fillna(prey_df['prey'])

# Sauvegarder prey.txt
prey_df[['prey', 'length', 'gene']].to_csv(PREY, sep='\t', header=False, index=False)

print(f"prey.txt généré avec succès sous : {PREY}")