from torchvision.transforms.functional_pil import _is_pil_image

from PIL import ImageEnhance
from config import Configuration

conf = Configuration()


def color_transform(img, color):
    """
    Modify the color of the image
    :param img: image to edit
    :param color: parameter for set the color
    :return: transformed image
    """
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color)

    return img


def brightness_transform(img, brightness):
    """
    Modify the brightness of the image
    :param img: image to edit
    :param brightness: parameter for set the brightness
    :return: transformed image
    """
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)

    return img


def contrast_transform(img, contrast):
    """
    Modify the contrast of the image
    :param img: image to edit
    :param contrast: parameter for set the contrast
    :return: transformed image
    """
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    return img


def sharpness_transform(img, sharpness):
    """
    Modify the sharpness of the image
    :param img: image to edit
    :param sharpness: parameter for set the sharpness
    :return: transformed image
    """
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness)

    return img
