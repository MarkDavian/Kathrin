from fastapi import APIRouter
from fastapi.responses import FileResponse

from db import db


router = APIRouter()


@router.get('/')
async def get_all_users():
    count, result = await db.get_documents(skip=0, limit=10)
    return {
        'status': 'OK',
        'result': {
            'count': count,
            'users': result
        }
    }


@router.get('/filter')
async def get_users_with_params(*, skip: int, limit: int):
    _, result = await db.get_documents(skip=skip, limit=limit)
    return {
        'status': 'OK',
        'result': result
    }

    
@router.get('/random')
async def get_random_user():
    result = await db.random_document()
    return {
        'status': 'OK',
        'result': result
    }


@router.get('/{syncId}')
async def get_user(syncId: int):
    user = await db.find(syncId)
    return {
        'status': 'OK',
        'result': user
    }


@router.get('/{syncId}/wct')
async def get_user_wct(syncId: int):
    wct = await db.get_user_wct(syncId)
    return {
        'status': 'OK',
        'result': wct
    }


@router.get('/{syncId}/avatar')
async def get_avatar(syncId: int):
    photo_path = await db.get_user_avatar(syncId)
    return FileResponse(path=f'avatars/{photo_path}')



