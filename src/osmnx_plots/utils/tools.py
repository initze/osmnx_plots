import random
import re


def list_to_random_number_dict(place_list):
    """
    Creates a dictionary with place names as keys and unique random numbers as values.

    :param place_list: List of place names
    :return: Dictionary {place: unique random number}
    """
    random_numbers = random.sample(range(1, len(place_list) + 1), len(place_list))
    return dict(zip(place_list, random_numbers))


# Sanitize place name for filename
def sanitize_filename(name):
    name = re.sub(r"[ ,]+", "_", name)
    name = re.sub(r"[^\w_]", "", name)
    return name.lower()
