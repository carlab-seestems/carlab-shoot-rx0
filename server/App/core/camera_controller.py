from loguru import logger
import gphoto2 as gp
import io
import time
from fastapi import HTTPException
import json
import os


class CameraController(object):
    def __init__(self):
        self.config = self._load_camera_config(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'camera_config.json'))

    def _load_camera(self, test_camera=False):
        logger.debug('Chargement de la caméra...')
        camera = gp.Camera()

        try:
            camera.init()
        except gp.GPhoto2Error as e:
            if e.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                logger.info(
                    'Aucune camera n\'as été trouvée ou un problème est survenu durant son initalisation. Essayez de la redemarrer')
                raise HTTPException(
                    status_code=400, detail='Aucune camera n\'as été trouvée ou un problème est survenu durant son initalisation. Essayez de redemarrer la camera ou de la reconnecter. Veuillez vérifier que la camera est bien en mode "PC Remote".')
            else:
                logger.error(e)
                raise e

        text = camera.get_summary()
        logger.info('La caméra a été chargée : {}'.format(text))
        if test_camera:
            camera.exit()
            logger.debug('Caméra détruite')
        else:
            return camera

    def _load_camera_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
        except Exception as e:
            logger.info(
                'Impossible de charger le fichier de configuration camera : {}'.format(e))
            raise HTTPException(
                status_code=400, detail='Impossible de charger le fichier de configuration camera : {}')
        return config

    def _set_camera_config(self, camera):
        main_widget = camera.get_config()

        for config in self.config['configs']:
            child = main_widget
            for child_name in config["name"].split('/')[2:]:
                child = child.get_child_by_name(child_name)
            child.set_value(config["value"])
            logger.debug('Config value {} set to {}'.format(
                config["name"], config["value"]))

        camera.wait_for_event(5000)
        time.sleep(5)
        camera.set_config(main_widget)

    def _take_and_save_picture(self, camera):
        try:
            #time.sleep(7)
            self._set_camera_config(camera)
            camera.trigger_capture()
            event = camera.wait_for_event(3000)
            count = 0
            while event[0] != 2:
                if count > 10:
                    e = Exception('Nombre de tentatives de prise de photo (10) dépassé.')
                    logger.error(e)
                    raise HTTPException(
                        status_code=400, detail="La photo n'a pas pu être prise : Nombre de tentatives de prise de photo (10) dépassé. ")
                if event[0] != 0:
                    camera.trigger_capture()
                    count += 1

                event = camera.wait_for_event(100)

                print(event)
            camera_filepath = event[1]
            #camera_filepath = camera.capture(gp.GP_CAPTURE_IMAGE)
            # camera_filepath = camera.trigger_capture()
            # camera.wait_for_event(10000)


        except Exception as e:

            camera.exit()

            logger.error(
                'La photo n\'a pas pu être prise : {}'.format(e))
            logger.error(e)
            raise HTTPException(
                status_code=400, detail="La photo n'a pas pu être prise")
        try:

            camera_file = camera.file_get(
                camera_filepath.folder, camera_filepath.name, gp.GP_FILE_TYPE_NORMAL)
        except Exception as e:
            camera.exit()
            logger.error(
                "Le fichier photo n'a pas pu être récupéré depuis la camera :".format(e))
            raise HTTPException(
                status_code=400, detail="Le fichier photo n'a pas pu être récupéré depuis la camera")
        logger.debug('Nom du fichier photo sur la caméra : {}'.format(
            camera_filepath.name))
        local_file = io.BytesIO(memoryview(camera_file.get_data_and_size()))
        local_file.seek(0)

        logger.debug('Fichier enregistré sous bytes.')

        camera.exit()
        return local_file

    def take_picture(self):
        camera = self._load_camera()

        buf = self._take_and_save_picture(camera)
        return buf

if __name__ == '__main__':
    camera = CameraController()
    for i in range(100):
        camera.take_picture()