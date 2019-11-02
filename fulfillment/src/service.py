from google.cloud import firestore
from response_formatter import ReponseFormatter

class Service:

    def __init__(self, request_parser_object):
        self.firestore_client = firestore.Client()
        self.request = request_parser_object

    def order_intent(self):

        user_id = self.request.userid
        parameters = self.request.parameters
        firestore_timestamp = firestore.SERVER_TIMESTAMP

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
                u'order_timestamp':firestore_timestamp,
                u'drinks': drinks_dict
            })
        else:
            current_item_count = 0
            item_number = current_item_count + 1
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref.set({
                u'current_item_count': item_number,
                u'order_timestamp':firestore_timestamp,
                u'drinks': {
                    drink_name: {
                        str(item_number): {
                            u'size': drink_size
                        }
                    }
                }
            })

        response = {'fulfillmentText': 'Your order is updated with item: '+drink_name + '. Do you want to add anything else?'}
        return response

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
        ## TODO - Remove the userID, complete order is dependent on this check

        # doc_ref_history=self.firestore_client.collection(u'history').document(user_id)
        # if doc_ref_history.get().exists is False:
        #     doc_ref_dict.update({u'closed_timestamp':self.firestore_timestamp})
        #     self.firestore_client.collection(u'history').document(user_id).set(doc_ref_dict)

        response_formatter = ReponseFormatter(drinks_dict)
        response_string = response_formatter.format_complete_order()
        print(response_string)

        # Return the response
        ## TODO Update the response
        response = {'fulfillmentText': 'Your order \n\n'+response_string+' \n\n is confirmed.'}
        return response

    def cancel_order_intent_yes(self):
        user_id = self.request.userid
        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            doc_ref.delete()
        response = {'fulfillmentText': 'Your order  is cancelled.'}
        return response

    def complete_order_intent(self):
        response = None
        user_id = self.request.userid
        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            response = {'fulfillmentText': 'Are you sure you want to place the order?'}
        else:
            response = {'fulfillmentText': 'There is nothing to cancel the order'}
        return response

    def complete_order_intent_yes(self):
        return self.order_intent_no()

    def cancel_item_intent_absent(self):

        user_id = self.request.userid
        parameters = self.request.parameters
        cancel_item_number = parameters.get('cancel_item')[0]

        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            drinks_dict = doc_ref.get().to_dict().get(u'drinks')

        # to check if item_number present in order
        item_number_set = set()
        for i in list(drinks_dict.keys()):
            item_number_set.add(list(drinks_dict[i].keys())[0])
        if cancel_item_number not in item_number_set:
            response = {'This item is not part of your order. Which item would you like to cancel?'}
        return response























