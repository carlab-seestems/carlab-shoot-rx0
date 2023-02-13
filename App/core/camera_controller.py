from loguru import logger
import gphoto2 as gp
import io


class CameraController(object):
    def __init__(self):
        pass

    def _load_camera(self, test_camera=False):
        logger.debug('Chargement de la caméra...')
        camera = gp.Camera()

        try:
            camera.init()
        except gp.GPhoto2Error as e:
            if e.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                logger.info(
                    'Aucune camera n\'as été trouvée ou un problème est survenu durant son initalisation. Essayez de la redemarrer')
                raise e
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

    def _take_picture_and_save_pictur(self, camera):
        try:
            camera_filepath = camera.capture(gp.GP_CAPTURE_IMAGE)
        except Exception as e:
            logger.error(
                'La photo n\'a pas pu être prise :'.format(e))
            raise Exception(
                'La photo n\'a pas pu être prise :') from e
        camera_file = camera.file_get(
            camera_filepath.folder, camera_filepath.name, gp.GP_FILE_TYPE_NORMAL)

        logger.debug('Nom du fichier photo sur la caméra : {}'.format(
            camera_filepath.name))

        local_file = io.BytesIO()
        camera_file.save(local_file)
        logger.debug('Fichier enregistré sous bytes.')

        return local_file
