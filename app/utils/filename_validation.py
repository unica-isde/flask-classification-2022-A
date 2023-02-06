ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """
    Check the extension of the file and ensure it's a png,
    jpg, jpeg or gif file.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
    The functions below are necessary to transform the
    upload image filename to a valid one.
    When an image filename containing brackets and blank spaces is uploaded,
    it is saved in the "uploads" folder without round brackets and 
    with underscores replacing the blank spaces.
"""


def rm_string_spaces(string):
    """
    It replaces every blank space in the string with an underscore.

    """
    return string.replace(" ", "_")


def rm_string_round_brackets(string):
    """
    It removes every round bracket from the filename.
    """
    return string.replace("(", "").replace(")", "")


def validate_filename(string):
    """
    A filename containing brackets and blank spaces is turned
    into a valid one.
    """
    tmp_string = rm_string_spaces(string)
    return rm_string_round_brackets(tmp_string)
