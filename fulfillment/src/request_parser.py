class RequestParser:

    def __init__(self, request):
        self.userid = u'myUserId'
        self.parameters = {}
        self.intent = {}
        self.output_contexts = {}
        self.__parse__(request)

    def __parse__(self, request):
        request_json = request.get_json(force=True)
        print(request_json)
        self.parameters = request_json.get('queryResult').get('parameters')
        self.intent = request_json.get('queryResult').get('intent')
        self.output_contexts = request_json.get('queryResult').get('outputContexts')
