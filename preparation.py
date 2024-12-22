import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Charger le dataset (malware dataset)
df = pd.read_csv(r'C:\Users\ANNA\Desktop\Malware.csv')

# Sélectionner uniquement les 7 premières caractéristiques pertinentes
features = df[['AddressOfEntryPoint', 'MajorLinkerVersion', 'MajorImageVersion',
               'MajorOperatingSystemVersion', 'DllCharacteristics',
               'SizeOfStackReserve', 'NumberOfSections']]

# Créer un scaler et ajuster les données
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Sauvegarder le scaler pour une utilisation future
joblib.dump(scaler, 'scaler_7_features.pkl')

# Afficher les premières données normalisées
print(scaled_features[:5])
