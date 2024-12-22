from app.app import app
from flask import render_template
import requests

@app.route('/retrieve_wikidata/<id>') # route avec 1 paramètre
def retrieve_wikidata(id):
    url = f'https://www.wikidata.org/wiki/Special:EntityData/{id}.json' # URL permettant d'accéder aux données d'un identifiant Wikidata
    response = requests.get(url) # utilisation de la fonction get pour interroger l'URL avec la bibliothèque requests

    # Cas où la requête permet d'obtenir les données de l'identifiant
    if response.status_code == 200: # le code HTTP 200 indique que la requête a fonctionnée
        data = response.json() # indique que l'on veut obtenir une réponse au format json
        # Rechercher les entités présentes dans les données
        entity_data = data.get('entities', {}).get(id)
        if entity_data:
            return render_template(
                'wikidata.html',
                id=id,
                metadonnees={
                    'status_code': response.status_code,
                    'content_type': response.headers.get('Content-Type')
                },
                data=entity_data
            )
    else:
        # Cas où aucune donnée n'est trouvée pour l'identifiant ou si le retour contient une erreur
        return render_template(
            'wikidata.html',
            id=id,
            metadonnees={
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type')
            },
            message_erreur=f'Aucune donnée valide n’a été retournée pour l’ID "{id}".' # Message d'erreur si aucune donnée n'est trouvée
        )
