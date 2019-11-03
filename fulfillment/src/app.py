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
    print(request)
    # Get the request object
    request_parser_object = RequestParser(request)

    service = Service(request_parser_object)
    if request_parser_object.intent["displayName"] == "order_intent":
        response_json = service.order_intent()
    elif request_parser_object.intent["displayName"] == "order_intent.no":
        response_json = service.order_intent_no()
    elif request_parser_object.intent["displayName"] == "cancel_item_intent":
        response_json = service.cancel_item_intent()
    elif request_parser_object.intent["displayName"] == "cancel_item_intent.continue":
        response_json = service.cancel_item_intent_continue()

    elif request_parser_object.intent["displayName"] == "cancel_order_intent.yes":
        response_json = service.cancel_order_intent_yes()
    elif request_parser_object.intent["displayName"] == "complete_order_intent":
        response_json = service.complete_order_intent()
    elif request_parser_object.intent["displayName"] == "complete_order_intent.yes":
        response_json = service.complete_order_intent_yes()


    # return response
    return make_response(jsonify(response_json))

# run the app
if __name__ == '__main__':
   app.run()