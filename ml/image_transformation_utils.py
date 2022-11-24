from torchvision.transforms.functional_pil import _is_pil_image

from ml.classification_utils import fetch_image
from PIL import ImageEnhance
from config import Configuration

conf = Configuration()


def color_transform(image_id, color):
    img = fetch_image(image_id)

    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color)

    return img


def image_save(img, img_id):
    image_name = img_id.replace('.JPEG', '_t.JPEG')
    image_path = conf.image_folder_path + '/' + image_name

    img.save(image_path, "JPEG")

    return image_name
