from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore

# initialize the flask app
app = Flask(__name__)
# default route

@app.route('/')
def index():
    return 'Hello World!'




#function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    print(req)
    # fetch action from json

    #PARAMETERS FROM DIALOGFLOW
    parameters =  req.get('queryResult').get('parameters')
    drinkName = parameters.get('drink')[0]
    drinkSize = parameters.get('size')[0]

    #FIRESTORE INTERACTIONS
    userId = u'myUserId'
    db = firestore.Client()
    doc_ref = db.collection(u'currentOrder').document(userId)
    currentItemCount = doc_ref.get().to_dict().get(u'currentItemCount')
    newCurrentItemCount = currentItemCount+1
    drinksDict = doc_ref.get().to_dict().get(u'drinks')
    if(drinksDict is None):
        drinksDict = dict()
    if drinkName in drinksDict:
        drinksDict.get(drinkName)[newCurrentItemCount]=drinkSize
    else:
        drinksDict[drinkName] = {newCurrentItemCount : drinkSize}

    doc_ref.update({
        u'currentItemCount' : newCurrentItemCount,
        u'drinks' : drinksDict
        # u'drink': parameters.get('drink')[0],
        # u'size': parameters.get('size')[0]
    })
    print( db.collection(u'users'))
    return {'fulfillmentText': 'This is a response from webhook.Hi'}


# def hit_firestore():


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()