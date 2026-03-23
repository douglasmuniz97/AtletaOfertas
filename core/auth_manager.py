import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_FILE = 'data/tokens.json'

def carregar_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None

def salvar_tokens(tokens_dict):
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens_dict, f, indent=4)

def realizar_refresh():
    print("🔄 Renovando Access Token...")
    tokens = carregar_tokens()
    if not tokens:
        return None

    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': tokens['refresh_token']
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        novos_tokens = response.json()
        dados_para_salvar = {
            "access_token": novos_tokens['access_token'],
            "refresh_token": novos_tokens.get('refresh_token', tokens['refresh_token'])
        }
        salvar_tokens(dados_para_salvar)
        return dados_para_salvar['access_token']
    return None

def requisicao_segura(url, metodo='GET', data=None):
    """
    Tenta fazer a requisição. Adiciona User-Agent para evitar Erro 403.
    """
    tokens = carregar_tokens()
    
    # Adicionamos o User-Agent aqui. 
    # Usamos uma string que simula um navegador real.
    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    if metodo == 'GET':
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, json=data)

    # Se o token expirou (Erro 401)
    if response.status_code == 401:
        novo_access_token = realizar_refresh()
        if novo_access_token:
            headers['Authorization'] = f'Bearer {novo_access_token}'
            if metodo == 'GET':
                return requests.get(url, headers=headers)
            else:
                return requests.post(url, headers=headers, json=data)
    
    return response