import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

# Chargement des données

data = np.loadtxt('normalized_data.csv', delimiter=',', skiprows=1)

data_7_features = data[:, :7] 
# Étape 1 : Normalisation des données
scaler = StandardScaler()
normalized_data = scaler.fit_transform(data_7_features )

# Étape 2 : Réduction de dimensions avec PCA
pca = PCA(n_components=3)  # Réduire à 5 dimensions
reduced_data = pca.fit_transform(normalized_data)

# Étape 3 : Sous-échantillonnage pour DBSCAN
subset_size = 5000  # Ajustez selon votre capacité mémoire
subset = reduced_data[np.random.choice(reduced_data.shape[0], size=subset_size, replace=False)]

# Étape 4 : Entraînement des modèles
# KMeans sur toutes les données réduites
print("Entraînement du modèle KMeans...")
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(reduced_data)

# DBSCAN sur le sous-échantillon
print("Entraînement du modèle DBSCAN...")
dbscan = DBSCAN(eps=1.0, min_samples=5)
dbscan.fit(subset)

# Étape 5 : Sauvegarde des modèles
joblib.dump(kmeans, 'kmeans_model.pkl')
joblib.dump(dbscan, 'dbscan_model.pkl')
print("Modèles sauvegardés avec succès.")

# Étape 6 : Sauvegarde des objets nécessaires pour API (PCA et Scaler)
joblib.dump(pca, 'pca_transform.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("PCA et Scaler sauvegardés.")
