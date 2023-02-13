from fastapi import APIRouter, HTTPException
from ..core.camera_controller import CameraController
from fastapi.responses import StreamingResponse

camera_controller = CameraController()
router = APIRouter()


@router.get('/', responses={200: {"content": {"image/jpeg": {}}}})
def take_picture(action):
    buf = camera_controller.take_picture()
    
        
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg",
    headers={'Content-Disposition': 'inline; filename="picture.jpg"'})

