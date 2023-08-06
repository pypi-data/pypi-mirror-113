from cg_learning_client.utils.HttpUtil import get_request
from cg_learning_client.utils.HttpUtil import get_or_exception
from cg_learning_client.utils.HttpUtil import post_request
import requests


class CGLearningClient:
    def __init__(self, endpoint, username: str = None, password: str = None):
        self.endpoint = endpoint
        self.username = username
        self.password = password

    def query_activity_by_name(self, name: str, exact: bool = True):
        response = get_request(self.endpoint, '/CG/xAPI/activities', params={
            'name': name,
            'exact': exact
        })
        if requests.codes.ok == response.status_code:
            return response.json()

    def query_activity(self, params=None):
        response = get_request(self.endpoint, '/xAPI/activities', params=params)
        if requests.codes.ok == response.status_code:
            return response.json()

    def query_statements(self, params=None):
        if params is None:
            params = {}
        response = get_or_exception(self.endpoint, '/xAPI/statements', params=params)
        return response

    def generate_operator(self, op_type: str, params: dict, source: list = None):
        operator = {
            'type': op_type,
            'params': params
        }
        if source is not None:
            operator['source'] = source
        response = post_request(self.endpoint, '/CG/xAPI/operator', params=None,
                                content_data=operator)
        if requests.codes.ok == response.status_code:
            return response.json()
        raise Exception("generate operator error")

    def query_operator_output(self, op_id: str, page=0, limit=20):
        response = post_request(self.endpoint, '/CG/xAPI/operator/output',
                                params={
                                    'operatorId': op_id,
                                    'page': page,
                                    'limit': limit
                                })
        if requests.codes.ok == response.status_code:
            return response.json()
        raise Exception("query operator output error")


class QueryParamsBuilder:
    def __init__(self):
        self.params = {}

    def set(self, key, value):
        if value is not None:
            self.params[key] = value
        return self

    def build(self):
        return self.params
