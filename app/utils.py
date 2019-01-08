import time
from flask import jsonify
from .extensions import parser
from marshmallow import fields, validate as validate_
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
now = int(time.time())


# def request_get(url, params=None):
#     """
#
#     Args:
#         url:
#         params:
#
#     Returns:
#
#     """
#     params = params or {}
#     response = requests.get(url, json=params)
#     if response.ok:
#         response = response.json()
#         return jsonify(response)
#     else:
#         code = response.status_code
#         response = response.json()
#         return jsonify(response), code
#
#
# def request_post(url, params=None):
#     """
#
#     Args:
#         url:
#         params:
#
#     Returns:
#
#     """
#     params = params or {}
#     response = requests.post(url, json=params)
#     if response.ok:
#         response = response.json()
#         return jsonify(response)
#     else:
#         code = response.status_code
#         response = response.json()
#         return jsonify(response), code


def parse_req(argmap):
    """
    Parser request from client
    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def send_result(data=None, message="OK", code=200, version=1):
    """
    Args:
        data: simple result object like dict, string or list
        message: message send to client, default = OK
        code: code default = 200
        version: version of api
    Returns:
        json rendered sting result
    """
    res = {
        "jsonrpc": "2.0",
        "status": True,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version(version)
    }

    return jsonify(res), 200


def send_error(data=None, message="Error", code=200, version=1):
    """"

    """
    res_error = {
        "jsonrpc": "2.0",
        "status": False,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version(version)
    }
    return jsonify(res_error), code


def get_version(version):
    """
    if version = 1, return api v1
    version = 2, return api v2
    Returns:

    """
    return "Crypto v2.0" if version == 2 else "Crypto v1.0"


class FieldString(fields.String):
    """
    validate string field, max length = 1024
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldString, self).__init__(validate=validate, **metadata)


class FieldNumber(fields.Number):
    """
    validate number field, max length = 30
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 30  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldNumber, self).__init__(validate=validate, **metadata)


def find_report_link(s):
    """
    Ge report link from url
    :param s:
    :return:
    """
    first = 'https://www.youtube.com/channel/'
    try:
        start = s.index(first) + len(first) + 2
        report_link = 'https://www.youtube.com/reportabuse?u={}'.format(s[start:])
        return report_link
    except ValueError:
        return None


def watch_videos(browser, href):
    ActionChains(browser) \
        .key_up(Keys.CONTROL) \
        .send_keys('t') \
        .key_up(Keys.CONTROL) \
        .perform()
    browser.get(href)
