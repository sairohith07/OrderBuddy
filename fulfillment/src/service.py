from google.cloud import firestore


class Service:

    def __init__(self, request_parser_object):
        self.firestore_client = firestore.Client()
        self.request = request_parser_object
        self.firestore_timestamp=firestore.SERVER_TIMESTAMP

    def order_intent(self):

        user_id = self.request.userid
        parameters = self.request.parameters
        

        # Assumption - Only one item per request.
        drink_name = parameters.get('drink')[0]
        drink_size = parameters.get('size')[0]

        # INSERT TO DB (If collection not present, it get's created)
        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref_dict = doc_ref.get().to_dict()

            current_item_count = doc_ref_dict.get(u'current_item_count')
            item_number = current_item_count + 1

            drinks_dict = doc_ref.get().to_dict().get(u'drinks')
            if drinks_dict is None:
                drinks_dict = {}

            if drink_name in drinks_dict:
                drinks_dict.get(drink_name)[str(item_number)] = {
                    u'size': drink_size
                }
            else:
                drinks_dict[drink_name] = {}
                drinks_dict[drink_name][str(item_number)] = {
                    u'size': drink_size
                }

            doc_ref.update({
                u'current_item_count': item_number,
                u'order_timestamp':self.firestore_timestamp,
                u'drinks': drinks_dict
            })
            response = {'fulfillmentText': 'Your order'+str(user_id)+'  is created'}
            return response
        else:
            current_item_count = 0
            item_number = current_item_count + 1
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref.set({
                u'current_item_count': item_number,
                u'order_timestamp':self.firestore_timestamp,
                u'drinks': {
                    drink_name: {
                        str(item_number): {
                            u'size': drink_size
                        }
                    }
                }
            })
            response = {'fulfillmentText': 'Your order'+str(user_id)+'  is updated.'}
            return response
            

    def order_intent_yes(self):
        print("Hi")

    def order_intent_no(self):
        response = None
        user_id = self.request.userid
        
        # Get the current order for the use
        doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
        doc_ref_dict = doc_ref.get().to_dict()
        drinks_dict = doc_ref.get().to_dict().get(u'drinks')
        if doc_ref.get().exists:
            doc_ref_n = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref_n.delete()
        ## TODO - Move the existing order from current order to history - (delete item_counter and add timestamp field
        doc_ref_history=self.firestore_client.collection(u'history').document(user_id)
        if doc_ref_history.get().exists is False:
            doc_ref_dict.update({u'closed_timestamp':self.firestore_timestamp})
            self.firestore_client.collection(u'history').document(user_id).set(doc_ref_dict)  

        # Return the response
        response = {'fulfillmentText': 'Your order '+str(drinks_dict)+' is confirmed.'}
        return response

    def cancel_order_intent(self):
        user_id = self.request.userid
        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref.delete()

    def cancel_item_intent(self):
        print("Hi")












