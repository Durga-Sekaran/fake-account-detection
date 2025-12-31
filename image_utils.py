from PIL import Image
import imagehash
import os

def image_check(image_folder):
    hashes = {}

    if not os.path.exists(image_folder):
        return hashes

    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        try:
            img = Image.open(image_path)
            hashes[image_name] = imagehash.phash(img)
        except:
            pass

    return hashes