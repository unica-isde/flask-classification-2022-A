from torchvision.transforms.functional_pil import _is_pil_image

from ml.classification_utils import fetch_image
from PIL import ImageEnhance
from config import Configuration

conf = Configuration()


def color_transform(img, color):
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color)

    return img


def brightness_transform(img, brightness):
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)

    return img


def contrast_transform(img, contrast):
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    return img


def sharpness_transform(img, sharpness):
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness)

    return img


def image_save(img, img_id):
    image_name = img_id.replace('.JPEG', '_t.JPEG')
    image_path = conf.image_folder_path + '/' + image_name

    img.save(image_path, "JPEG")

    return image_name
