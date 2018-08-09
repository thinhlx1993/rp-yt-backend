import requests
import time
import re
import datetime
import time
import urllib.request
from flask import jsonify
from .extensions import parser
from marshmallow import fields, validate as validate_
from dateutil.parser import parse

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}
IGNORE_LATING = {'!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '.', '/', '\\', '{', '}', '`',
                 '~', ':', '"', '<', '>', '?', ';', "'", '=', '-', "– ", "“", "„", "‘"}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif'}
# stop_words = set(stopwords.words('german'))
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
now = int(time.time())


def request_get(url, params=None):
    """

    Args:
        url:
        params:

    Returns:

    """
    params = params or {}
    response = requests.get(url, json=params)
    if response.ok:
        response = response.json()
        return jsonify(response)
    else:
        code = response.status_code
        response = response.json()
        return jsonify(response), code


def request_post(url, params=None):
    """

    Args:
        url:
        params:

    Returns:

    """
    params = params or {}
    response = requests.post(url, json=params)
    if response.ok:
        response = response.json()
        return jsonify(response)
    else:
        code = response.status_code
        response = response.json()
        return jsonify(response), code


def parse_req(argmap):
    """
    Parser request from client
    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def find_prev_next(elem, elements):
    """

    Args:
        elem:
        elements:

    Returns:

    """
    previous, next_item, index = None, None, None
    if elem in elements:
        index = elements.index(elem)
    # if index and index > 0:
    #     previous = elements[index - 1]
    # if index and index < (len(elements)-1):
    #     next_item = elements[index + 1]

    l = len(elements)
    for index, obj in enumerate(elements):
        if obj == elem:
            if index > 0:
                previous = elements[index - 1]
            if index < (l - 1):
                next_item = elements[index + 1]
    return previous, next_item


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


def format_desc(des):
    """ for mat description for send result or error json to client

    Args:
        des:

    Returns:

    """
    des = des.replace('\n', '<br/>')
    return des


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_keyword(article, keyword):
    """
    Allow search keyword with two character in title abstract or content of article
    :param article:
    :param keyword:
    :return:
    """
    list_keyword = []
    keywords = article.keywords
    keywords = keywords.lower().split(', ')

    for item in keywords:
        if item.startswith(keyword) and item.title() not in list_keyword:
            list_keyword.append(item.title())

    return list_keyword


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def process_keyword(keyword):
    """
    Need to replace keyword to separate keyword
    eg: Thema\nquartalszahlen to Thema quartalszahlen
    :param keyword:
    :return:
    """
    return keyword.replace("\n", ' ')


def convert_object_id(data):
    """
    Use for convert ObjectId to string
    :param data:
    :return:
    """
    data = list(data)
    for el in data:
        el['_id'] = str(el['_id'])
    return data


def parse_date_from_string(text):
    date_text = re.findall(r'(?:\d\d|\d)(?:.\s|\s|.)(?:1|2|3|4|5|6|7|8|9|01|02|03|04|05|06|07|08|09|10|11|12|Januar|Februar|März|April|Mai|Juni|August|September|Oktober|November|Dezember|Jan|Feb|Mar|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)(?:.\s|\s|.)\d{4}', text)
    if len(date_text) > 0:
        date = date_text[0]
        date = date.replace(" ", ".")
        date = date.replace("..", ".")
        list_time_split = date.split(".")
        if list_time_split[1] == 'Januar' or list_time_split[1] == 'Jan':
            list_time_split[1] = '01'
        elif list_time_split[1] == 'Februar' or list_time_split[1] == 'Feb':
            list_time_split[1] = '02'
        elif list_time_split[1] == 'März' or list_time_split[1] == 'Mar':
            list_time_split[1] = '03'
        elif list_time_split[1] == 'April' or list_time_split[1] == 'Apr':
            list_time_split[1] = '04'
        elif list_time_split[1] == 'Mai' or list_time_split[1] == 'Mai':
            list_time_split[1] = '05'
        elif list_time_split[1] == 'Juni'or list_time_split[1] == 'Jun':
            list_time_split[1] = '06'
        elif list_time_split[1] == 'Juli' or list_time_split[1] == 'Jul':
            list_time_split[1] = '07'
        elif list_time_split[1] == 'August' or list_time_split[1] == 'Aug':
            list_time_split[1] = '08'
        elif list_time_split[1] == 'September' or list_time_split[1] == 'Sep':
            list_time_split[1] = '09'
        elif list_time_split[1] == 'Oktober'or list_time_split[1] == 'Okt':
            list_time_split[1] = '10'
        elif list_time_split[1] == 'November' or list_time_split[1] == 'Nov':
            list_time_split[1] = '11'
        elif list_time_split[1] == 'Dezember'or list_time_split[1] == 'Dez':
            list_time_split[1] = '12'

#           2018-02-03 00:00:00
        try:
            new_datetime = datetime.datetime(int(list_time_split[2]), int(list_time_split[1]), int(list_time_split[0]),
                                             0, 0, 0, 0, tzinfo=datetime.timezone.utc)
            return int(new_datetime.timestamp())
        except Exception as ex:
            return None
    else:
        try:
            # new_datetime = parser.parse(text)
            new_datetime = parse(text)
            new_datetime = new_datetime.replace(tzinfo=datetime.timezone.utc)
            return int(new_datetime.timestamp())
        except Exception as ex:
            return None
