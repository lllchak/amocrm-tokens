import requests
import time
from app.models.token import Token
from app.core.config import settings
from app.db.session import get_db_connection


def get_amocrm_tokens(auth_code: str, client_id: str, domain: str) -> Token:
    url = f'https://{domain}/oauth2/access_token'

    payload = {
        'client_id': client_id,
        'client_secret': settings.amocrm_client_secret,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': settings.amocrm_redirect_uri
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    tokens = response.json()
    save_tokens_db(tokens)

    return Token(**tokens)


def save_tokens_db(tokens: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    expires_in = int(time.time()) + tokens['expires_in']

    cursor.execute('''
        INSERT INTO amocrm_tokens (access_token, refresh_token, expires_in) 
        VALUES (%s, %s, %s)
    ''', (tokens['access_token'], tokens['refresh_token'], expires_in))

    conn.commit()
    cursor.close()
    conn.close()


def get_valid_token() -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT access_token, refresh_token, expires_in FROM amocrm_tokens ORDER BY id DESC LIMIT 1')
    token = cursor.fetchone()

    cursor.close()
    conn.close()

    if token:
        access_token, refresh_token, expires_in = token
        if time.time() > expires_in:
            return refresh_tokens(refresh_token)
        return access_token, refresh_token
    else:
        return 'Not found'


def refresh_tokens(refresh_token: str) -> str:
    url = f'https://{settings.amocrm_subdomain}/oauth2/access_token'

    payload = {
        'client_id': settings.amocrm_client_id,
        'client_secret': settings.amocrm_client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': settings.amocrm_redirect_uri
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    tokens = response.json()
    save_tokens_db(tokens)

    return tokens['access_token']