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

    if request_parser_object.intent["displayName"] == "order_intent":
        response_json = Service.order_intent(request_parser_object)
    elif request_parser_object.intent["displayName"] == "order_intent.no":
        response_json = Service.order_intent_no(request_parser_object)
    elif request_parser_object.intent["displayName"] == "cancel_item_intent":
        response_json = Service.cancel_item_intent(request_parser_object)
    elif request_parser_object.intent["displayName"] == "cancel_item_intent.continue":
        response_json = Service.cancel_item_intent_continue(request_parser_object)

    elif request_parser_object.intent["displayName"] == "cancel_order_intent.yes":
        response_json = Service.cancel_order_intent_yes(request_parser_object)
    elif request_parser_object.intent["displayName"] == "complete_order_intent":
        response_json = Service.complete_order_intent(request_parser_object)
    elif request_parser_object.intent["displayName"] == "complete_order_intent.yes":
        response_json = Service.complete_order_intent_yes(request_parser_object)
    elif request_parser_object.intent["displayName"] == "Default Welcome Intent":
        response_json = Service.default_welcome_intent(request_parser_object)
    elif request_parser_object.intent["displayName"] == 'sign_in_intent':
        response_json = Service.sign_in_intent(request_parser_object)
    elif request_parser_object.intent["displayName"]== 'Default Fallback Intent':
        response_json = Service.fallback_intent(request_parser_object)

    response = make_response(jsonify(response_json))
    return response

# run the app
if __name__ == '__main__':
   app.run()