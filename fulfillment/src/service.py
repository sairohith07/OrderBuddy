from google.cloud import firestore

class Service:

    def __init__(self, request_parser_object):
        self.firestore_client = firestore.Client()
        self.request = request_parser_object

    def order_intent(self):

        user_id = self.request.userid
        parameters = self.request.parameters

        # Assumption - Only one item per request.
        drink_name = parameters.get('drink')[0]
        drink_size = parameters.get('size')[0]

        # INSERT TO DB (If collection not present, it get's created)
        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists == True:
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref_dict = doc_ref.get().to_dict()

            current_item_count = doc_ref_dict.get(u'current_item_count')
            item_number = current_item_count + 1

            drinks_dict = doc_ref.get().to_dict().get(u'drinks')
            if (drinks_dict is None):
                drinks_dict = dict()
            if drink_name in drinks_dict:
                drinks_dict.get(drink_name)[item_number] = drink_size
            else:
                drinks_dict[drink_name] = {item_number: drink_size}

            doc_ref.update({
                u'currentItemCount': item_number,
                u'drinks': drinks_dict
                # u'drink': parameters.get('drink')[0],
                # u'size': parameters.get('size')[0]
            })
        else:
            current_item_count = 0
            item_number = current_item_count + 1
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref.set({
                u'currentItemCount': item_number,
                u'drinks': {
                    drink_name: {
                        str(item_number): {
                            u'size': drink_size
                        }
                    }
                }
            })

        return {'fulfillmentText': 'This is a response from webhook.Hi'}

    def cancel_order_intent(self):
        print("Hi")

    def cancel_item_intent(self):
        print("Hi")



