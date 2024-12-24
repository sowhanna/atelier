from flask import Flask, request, jsonify ,render_template
import joblib
import numpy as np
import os
from extract import script_extract

app = Flask(__name__)

# Charger le scaler, PCA et le modèle KMeans
scaler = joblib.load('scaler.pkl')
pca = joblib.load('pca_transform.pkl')
kmeans = joblib.load('kmeans_model.pkl')

@app.route('/') 
def home(): 
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print(f"Requête reçue : {request}")
    print(f"Clés dans request.files : {list(request.files.keys())}")
    print(f"Clés dans request.form : {list(request.form.keys())}")

    file_key = 'File' if 'File' in request.files else 'file'
    if file_key not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files[file_key]
    try:
        file_path = os.path.join('temp', file.filename)
        file.save(file_path)
        
        features = script_extract(file_path)
        if features is None:
            return jsonify({'error': 'Échec de l\'extraction des caractéristiques'}), 400

        features_array = np.array(list(features.values())).reshape(1, -1)
        features_7 = features_array[:, :7]
        features_normalized = scaler.transform(features_7)
        features_reduced = pca.transform(features_normalized)
        prediction = kmeans.predict(features_reduced)
        result = "LEGITIME" if prediction[0] == 1 else "MALEWARE"

        return jsonify({
            'prediction': result,
            'normalized_features': features_normalized.tolist()
        })
    except Exception as e:
        print(f"Erreur lors du traitement du fichier: {str(e)}")
        return jsonify({'error': f'Erreur lors du traitement du fichier: {str(e)}'}), 500

if __name__ == '__main__':
    # Créer un dossier temporaire pour les fichiers téléchargés si nécessaire
    os.makedirs('temp', exist_ok=True)
    # Lancer l'API Flask
    app.run(debug=True)
