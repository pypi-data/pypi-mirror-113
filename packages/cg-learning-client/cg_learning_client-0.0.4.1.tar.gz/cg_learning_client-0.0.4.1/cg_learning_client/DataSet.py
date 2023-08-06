import cg_learning_client.CGLearningClient as Client


class CGData:
    Page = "page"
    Limit = "limit"
    Id = "id"

    def __init__(self):
        self._page = 1
        self._limit = 100
        self._total = None
        self._lazyLoad = True
        self._data_segment = {}
        self._client = None

    def __iter__(self):
        return DataSegmentIterator(self, self._total)

    def __len__(self):
        return self._total

    def __getitem__(self, item):
        import numbers
        if isinstance(item, slice):
            return [self[ii] for ii in range(*item.indices(len(self)))]
        elif isinstance(item, numbers.Integral):
            return self._get_by_index(item)

    def _get_by_index(self, index):
        page = int(index / self._limit)
        if page not in self._data_segment:
            # page missing
            self._on_page_missing(page)
        return self._data_segment[page][index % self._limit]

    def _on_page_missing(self, page):
        pass


class DataSegmentIterator:
    def __init__(self, data: CGData, total=None):
        self.__data = data
        self.__start = 0
        self.__end = 0
        if total is not None:
            self.__end = total

    def __next__(self):
        if self.__start >= self.__end:
            raise StopIteration
        self.__start += 1
        return self.__data[self.__start - 1]


class CGStatementData(CGData):
    StatementIdParam = "statementId"
    AgentParam = "agent"
    Verb = "verb"
    Activity = "activity"
    Registration = "registration"
    Since = "since"
    Until = "until"
    Format = "format"
    RelatedActivities = "relatedActivities"
    RelatedAgents = "relatedAgents"
    RelatedStatements = "relatedStatements"
    Attachments = "attachments"
    Ascending = "ascending"

    def __init__(self, client: Client, query_params: dict = None):
        super().__init__()
        self.__client = client
        self.__params = query_params
        self._total = 0
        self.headers = None
        self.headers_op = None
        import copy
        params = {}
        if self.__params is not None:
            params = copy.deepcopy(self.__params)
        params[CGData.Page] = 0
        params[CGData.Limit] = 1
        self._total = int(self.__client.query_statements(params)["total"])

    # def __iter__(self):
    #     return DataSegmentIterator(self, self._total)

    # def __len__(self):
    #     return self._total

    # def __getitem__(self, item):
    #     import numbers
    #     if isinstance(item, slice):
    #         return [self[ii] for ii in range(*item.indices(len(self)))]
    #     elif isinstance(item, numbers.Integral):
    #         return self.__get_by_index(item)
    #

    def _on_page_missing(self, page):
        self.__params[CGData.Page] = page
        if CGData.Limit not in self.__params:
            self.__params[CGData.Limit] = self._limit
        else:
            self._limit = self.__params[CGData.Limit]
        response = self.__client.query_statements(self.__params)
        self._total = int(response["total"])
        self._data_segment[page] = response["statements"]

    def get_available_headers(self):
        if self.headers is not None:
            return self.headers
        self.headers_op = self.__client.generate_operator('Query', self.__params)
        self.headers = self.__client.query_operator_output(self.headers_op['id'])
        return self.headers

    def get_structured_data(self, headers: list = None):
        if self.headers is None:
            tmp = self.get_available_headers()
            if headers is None:
                headers = tmp
            print(self.headers_op['id'])
        operator = self.__client.generate_operator('Select', {
            'headers': headers
        }, source=[self.headers_op['id']])
        return self.__client.query_operator_output(operator['id'])


class CGActivityData(CGData):
    Name = "name"
    RelatedActivities = "relatedActivities"
    Exact = "exact"
    Activities = "activities"

    def __init__(self, client: Client, query_params: dict = None):
        super().__init__()
        self.__client = client
        self.__params = query_params
        self._total = 0
        import copy
        params = {}
        if self.__params is not None:
            params = copy.deepcopy(self.__params)
        params[CGData.Page] = 0
        params[CGData.Limit] = 1
        print(params)
        self._total = int(self.__query_activity(params)["total"])

    def __query_activity(self, params: dict = None):
        if CGActivityData.Name in params.keys():
            exact = params[CGActivityData.Exact] if CGActivityData.Exact in params.keys() else True
            activity_list = self.__client.query_activity_by_name(params[CGActivityData.Name], exact)
            if activity_list is not None:
                self._data_segment[0] = activity_list
            else:
                self._data_segment[0] = []
            import sys
            return {"total": len(self._data_segment[0]), CGActivityData.Activities: activity_list, CGData.Page: 0,
                    CGData.Limit: sys.maxsize}
        return self.__client.query_activity(params)

    def _on_page_missing(self, page):
        if CGActivityData.Name in self.__params.keys():
            raise RuntimeError("name query for activity should not miss page")
        self.__params[CGData.Page] = page
        if CGData.Limit not in self.__params:
            self.__params[CGData.Limit] = self._limit
        else:
            self._limit = self.__params[CGData.Limit]
        response = self.__client.query_activity(self.__params)
        self._total = int(response["total"])
        self._data_segment[page] = response[CGActivityData.Activities]


class StructuredData(CGData):
    def __init__(self):
        super().__init__()
