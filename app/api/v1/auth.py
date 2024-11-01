from fastapi import APIRouter
from app.services.access_token import get_amocrm_tokens

router = APIRouter()


@router.get('/authorize')
async def authorize(code: str, referer: str, client_id: str):
    token = get_amocrm_tokens(code, client_id, referer)

    return {'access_token': token.access_token, 'refresh_token': token.refresh_token}
