from fastapi import APIRouter

router = APIRouter()


@router.get('/take_picture', responses={200: {"content": {"image/jpeg": {}}}})
def take_picture():
    return {'message': 'Taking a picture'}
