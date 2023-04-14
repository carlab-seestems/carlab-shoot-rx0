from fastapi import APIRouter, HTTPException, Response
from ..core.camera_controller import CameraController
from fastapi.responses import StreamingResponse

camera_controller = CameraController()
router = APIRouter()


@router.get('/', responses={200: {"content": {"image/jpeg": {}}}})
def take_picture(action):
    buf = camera_controller.take_picture()

    buf.seek(0)
    return Response(content=buf.read(), media_type="image/jpeg")

@router.get('/set_iso', responses={200: {"content": {"image/jpeg": {}}}})
def take_picture(iso): 
    camera_controller.set_iso(iso)