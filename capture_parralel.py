from joblib import Parallel, delayed
import requests
from io import BytesIO
from PIL import Image
import os
from argparse import ArgumentParser
import json


def get_and_process_picture(config, main_foler, widths_config, crops_config=None):
    try:
        r = requests.get(config['url'], timeout=15)
    except requests.exceptions.Timeout:
        raise Exception("Timeout of 15sec with url: " + config['url'])
    if (r.status_code != 200):
        raise Exception("Error with url: " + config['url'])
    img = Image.open(BytesIO(r.content))

    for width in widths_config:
        # verify if folder exists
        folder_width = os.path.join(main_foler, str(width))
        if not os.path.exists(folder_width):
            os.makedirs(folder_width)
        img_temp = img.copy()
        img_temp.thumbnail((width, width), Image.Resampling.LANCZOS)
        img_temp.save(os.path.join(
            folder_width, str(config['viewId']) + '.jpg'))


parser = ArgumentParser()

parser.add_argument('--widths', type=int, nargs='+', default=[1920, 640, 320])
parser.add_argument('--folder', type=str, default='./test')
parser.add_argument('--config', type=str, default='./config.json')

args = parser.parse_args()

try:
    with open(args.config, 'r') as file:
        config = json.load(file)
except Exception as e:
    raise Exception(
        'Impossible de charger le fichier de configuration : {}'.format(args.config))

Parallel(n_jobs=len(config))(delayed(get_and_process_picture)(c, args.folder, args.widths)
                             for c in config)
