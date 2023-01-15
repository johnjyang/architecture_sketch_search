import os
from PIL import Image, UnidentifiedImageError

def get_file_list(root_dir):

    file_list = []
    counter = 1
    extensions = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']

    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(ext in filename for ext in extensions):
                file_list.append(os.path.join(root, filename))
                counter += 1

    file_list = sorted(file_list)

    return file_list


images = get_file_list('arch_100k_dataset_sketches')
images.reverse()

for path in images:
    try:
        im = Image.open(path)
        print(im.verify(), path)
    except UnidentifiedImageError:
        os.remove(path)
