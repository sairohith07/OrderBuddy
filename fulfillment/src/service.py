from google.cloud import firestore

class Service:

    def __init__(self, request_parser_object):
        self.firestore_client = firestore.Client()
        self.request = request_parser_object

    def order_intent(self):

        userId = self.request.userid

        parameters = self.request.parameters
        drink_name = parameters.get('drink')[0]
        drink_size = parameters.get('size')[0]

        # INSERT TO DB
        doc_ref = self.firestore_client.collection(u'currentOrder').document(userId)
        print(self.firestore_client.collection(u'users'))
        current_item_count = doc_ref.get().to_dict().get(u'currentItemCount')
        item_number = current_item_count + 1

        drinks_dict = doc_ref.get().to_dict().get(u'drinks')
        if (drinks_dict is None):
            drinks_dict = {}
        if drink_name in drinks_dict:
            drinks_dict.get(drink_name)[str(item_number)] = drink_size
        else:
            drinks_dict[drink_name] = {}
            drinks_dict[drink_name][str(item_number)] = drink_size
                # {item_number: drink_size}

        print("---------------")
        print(drinks_dict)

        doc_ref.update({
            u'currentItemCount': item_number,
            u'drinks': drinks_dict
        })

        print(self.firestore_client.collection(u'users'))
        return {'fulfillmentText': 'This is a response from webhook.Hi'}

    def cancel_order_intent(self):
        print("Hi")

    def cancel_item_intent(self):
        print("Hi")



