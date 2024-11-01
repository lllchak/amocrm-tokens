from fastapi import APIRouter
from app.services.access_token import get_valid_token

router = APIRouter()


@router.get('/get_token')
def get_token():
    access_token, refresh_token = get_valid_token()

    return {'access_token': access_token, 'refresh_token': refresh_token}
