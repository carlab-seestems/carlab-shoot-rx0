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
def set_iso(iso):
    camera_controller.set_iso(iso)


@router.get('/set_color_temp', responses={200: {"content": {"image/jpeg": {}}}})
def set_color_temp(temp):
    camera_controller.set_temp(temp)


@router.get('/set_shutter_speed', responses={200: {"content": {"image/jpeg": {}}}})
def set_shutter_speed(shutter_speed):
    camera_controller.set_shutter_speed(shutter_speed)
