from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
from extract import script_extract

app = Flask(__name__)

# Charger le scaler et le modèle (le modèle sera utilisé pour la prédiction si nécessaire)
scaler = joblib.load('scaler.pkl')

# Charger le modèle KMeans
kmeans = joblib.load('kmeans_model.pkl')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API en ligne. Utilisez la route POST /predict pour prédire."})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files['file']

    try:
        # Sauvegarder temporairement le fichier téléchargé
        file_path = os.path.join('temp', file.filename)
        file.save(file_path)

        # Extraire les caractéristiques du fichier PE (supposons que 'script_extract' retourne un dictionnaire)
        features = script_extract(file_path)

        if features is None:
            return jsonify({'error': 'Échec de l\'extraction des caractéristiques'}), 400

        # Convertir les caractéristiques en tableau numpy
        features_array = np.array(list(features.values())).reshape(1, -1)

        # Sélectionner uniquement les 7 premières caractéristiques
        features_7 = features_array[:, :7]  # Sélection des 7 premières caractéristiques

        # Normaliser les caractéristiques avec le scaler
        features_normalized = scaler.transform(features_7)

        # Effectuer la prédiction avec KMeans
        prediction = kmeans.predict(features_normalized)

        # Afficher le résultat de la prédiction
        result = "Malware" if prediction[0] == 1 else "Légitime"

        return jsonify({
            'prediction': result,
            'normalized_features': features_normalized.tolist()
        })

    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement du fichier: {str(e)}'}), 500

if __name__ == '__main__':
    # Créer un dossier temporaire pour les fichiers téléchargés si nécessaire
    os.makedirs('temp', exist_ok=True)

    # Lancer l'API Flask
    app.run(debug=True)
