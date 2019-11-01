from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from request_parser import RequestParser
from service import Service

# initialize the flask app
app = Flask(__name__)
# default route

@app.route('/')
def index():
    return 'Hello World!'

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    response_json = None

    # Get the request object
    request_parser_object = RequestParser(request)

    service = Service(request_parser_object)
    if request_parser_object.intent["displayName"] == "order.intent":
        response_json = service.order_intent()
    elif request_parser_object.intent["displayName"] == "order.intent.no":
        response_json = service.order_intent_no()

    # return response
    return make_response(jsonify(response_json))

# run the app
if __name__ == '__main__':
   app.run()