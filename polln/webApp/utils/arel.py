import os
import json
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Arel():
    def get_token(self,user,pwd):
        """
            recupere un token de l'api d'arel si le user et le mot de passe correspondent
        """
        #on charge les identifiants pour se connecter à l'api d'arel (il faudrait faire un try catch...)
        json_data=open(BASE_DIR+'/keyArel.json')
        if(json_data):
            data = json.load(json_data)
            key = data['key']
            app = data['app']
            data = {
                        'grant_type':'password',
                        'username':user,
                        'password':pwd,
                        'scope':'read',
                        'format':'json'
                    }
            # on envoi la requete et on la recupere en json.
            http_response = requests.post('https://arel.eisti.fr/oauth/token', data = data,auth=(app, key))
            # throw une json.decoder.JSONDecodeError en cas de mauvais identifiants
            http_response_json = http_response.json()
            # si on recoit un token c'est bon
            if ('access_token' in http_response_json.keys()):
                return http_response_json['access_token']
        return False

    def requete_arel(self,url_api,token):
        """
        fait une requete sur l'api d'arel et renvoi le résultat en json (le token doit être valide)
        """
        headers = {'Accept':'application/json','AUTHORIZATION':'Bearer '+token}
        data = {
                'format':'json',
            }
        http_response = requests.get('https://arel.eisti.fr/'+url_api,headers = headers,data=data)
        return http_response.json()