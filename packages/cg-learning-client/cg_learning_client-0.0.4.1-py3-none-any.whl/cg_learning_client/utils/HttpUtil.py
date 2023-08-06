import requests
import urllib.parse


def url_join_args(endpoint, api, params: dict=None, **kwargs):
    """拼接请求参数
    :param endpoint: 服务地址
    :param api: 接口，可带?或不带
    :param params: 请求参数
    :param kwargs: 未出现的参数，将组合成字典
    :return: 拼接好的url
    """
    result = endpoint + api
    if not result.endswith('?') and (params or kwargs):
        result = result + '?'
    if params:
        result = result + urllib.parse.urlencode(params)
    if kwargs:
        if params:
            result = result + '&' + urllib.parse.urlencode(kwargs)
        else:
            result = result + urllib.parse.urlencode(kwargs)
    return result


def get_request(endpoint, api, params: dict = None, headers: dict = None):
    """发起一个GET请求
    :param endpoint: 服务地址
    :param api: 接口，可带?或不带
    :param params: 请求参数
    :param headers: 请求头
    :return: 拼接好的url
    """
    url = url_join_args(endpoint, api, params)
    return requests.get(url, headers=headers)


def post_request(endpoint, api, params: dict = None, content_data:dict=None, headers: dict = None):
    """发起一个POST请求
    :param endpoint: 服务地址
    :param api: 接口，可带?或不带
    :param params: 请求参数
    :param content_data: 要上传的非文件对象
    :param headers: 请求头
    :return: 拼接好的url
    """
    url = url_join_args(endpoint, api, params)
    return requests.post(url, json=content_data, headers=headers)


def get_or_exception(endpoint, api, params: dict = None, headers: dict = None):
    response = get_request(endpoint, api, params, headers)
    if requests.codes.ok == response.status_code:
        return response.json()
