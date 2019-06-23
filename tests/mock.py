"""
lite_cache/tests mock.py
"""
import os
import random
import string


def random_str(str_len: int) -> str:
    """

    Args:
        str_len:

    Returns:

    """
    assert str_len, 'str_len cannot be blank'
    assert isinstance(str_len, int), 'str_len must be an int'

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(str_len))


def get_random_key():
    return random_str(12)


def get_mock_int():
    # Return random number
    return 1


def get_mock_str():
    # Return random str
    return random_str(32)


def get_mock_dict():
    mock = dict()
    test_types = [get_mock_int, get_mock_str]

    for _ in range(random.randint(2, 5)):
        typ = random.choice(test_types)
        mock[get_random_key()] = typ()

    return mock


def random_data():
    data = os.urandom(2 ** 13)
    return data
