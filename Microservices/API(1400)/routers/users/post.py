import aiohttp
from fastapi import APIRouter, UploadFile

from models import NewUser
from config import settings


router = APIRouter()


@router.post("/users/{syncId}/avatar")
async def create_user_avatar(syncId: int, file: UploadFile):
    """
    {
        'status': 'OK',
        'result': str (filename)
    }
    """
    file_bytes = await file.read()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.users+settings.Methods.Users.Post.avatar(syncId=syncId),
            data=file_bytes
        ) as resp:
            r = await resp.json()

    return r


