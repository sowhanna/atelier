
import requests

# L'URL de votre API Flask
url = 'http://127.0.0.1:5000/predict'

# Le chemin vers le fichier PE à envoyer
file_path = 'C:/Windows/System32/notepad.exe'  # Suppression de la virgule ici

# Ouvrir le fichier en mode binaire
with open(file_path, 'rb') as file:
    files = {'file': file}
    
    # Envoyer une requête POST avec le fichier
    response = requests.post(url, files=files)

    # Vérifier la réponse de l'API
    if response.status_code == 200:
        print("Réponse de l'API:", response.json())
    else:
        print(f"Erreur {response.status_code}: {response.text}")
