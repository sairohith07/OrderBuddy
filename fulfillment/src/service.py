from google.cloud import firestore
from response_formatter import ResponseFormatter


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

        response = {'fulfillmentText': 'Your order is updated with a ' + drink_size + ' ' + drink_name + '. Do you want to add anything else?'}

        return response

    def order_intent_no(self):
        response = None
        user_id = self.request.userid

        # Get the current order for the user
        doc_ref_current_order = self.firestore_client.collection(u'current_order').document(user_id)
        if doc_ref_current_order.get().exists:

            # create key  closed timestamp for the order
            doc_ref_current_order.update({u'closed_timestamp': firestore.SERVER_TIMESTAMP})
            doc_ref_dict = doc_ref_current_order.get().to_dict()

            # remove from current_order collection and move to history collection

            del doc_ref_dict[u'current_item_count']
            drinks_dict = doc_ref_current_order.get().to_dict().get(u'drinks')

            doc_ref_history = self.firestore_client.collection(u'history').document(user_id)
            if doc_ref_history.get().exists:
                orders_dict = doc_ref_history.get().to_dict().get(u'orders')
                if orders_dict is None:
                    doc_ref_history.set({u'orders': [doc_ref_dict]})
                else:
                    doc_ref_history.update({u'orders': firestore.ArrayUnion([doc_ref_dict])})
            else:
                doc_ref_history.set({u'orders': [doc_ref_dict]})

            # delete from current_order
            doc_ref_current_order.delete()

            response_formatter = ResponseFormatter(drinks_dict)
            response_string = response_formatter.format_complete_order()
            response = {'fulfillmentText': 'Your order \n\n' + response_string + ' \n\n is confirmed.'}
        else:
            response = {'fulfillmentText': 'There is no existing order to delete'}

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
            response = {'fulfillmentText': 'Your cart is empty. Add some items !!'}
        return response

    def complete_order_intent_yes(self):
        return self.order_intent_no()


    def cancel_item_intent(self):
        user_id = self.request.userid
        parameters = self.request.parameters

        print(parameters)

        doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
        doc_ref_dict = doc_ref.get().to_dict()
        drinks_dict = doc_ref_dict.get(u'drinks')
        current_item_count = doc_ref_dict.get(u'current_item_count')



        if(len(parameters['drink'])>0 and parameters['drink'] in drinks_dict and len(drinks_dict[parameters['drink']])>0 ):
            response_formatter_object = ResponseFormatter({parameters['drink']: drinks_dict[parameters['drink']]})
            response = response_formatter_object.format_cancel_intent_response()

        elif(len(parameters['drink']) == 0 or len(drinks_dict[parameters['drink']])==0):
            drink_desc = ""
            last_item_stat = False
            for each_category in drinks_dict:
                drinks_in_category = drinks_dict[each_category]
                for each_item_num in drinks_in_category:
                    if(each_item_num == current_item_count):
                        drink_desc += drinks_in_category[each_item_num]['size']+" "+each_category
                        last_item_stat = True

            if not last_item_stat:
                current_item_count = 1
                for each_category in drinks_dict:
                    drinks_in_category = drinks_dict[each_category]
                    for each_item_num in drinks_in_category:
                        if(int(each_item_num))>current_item_count:
                            current_item_count = int(each_item_num)
                            drink_desc = drinks_in_category[each_item_num]['size'] + " " + each_category

            doc_ref.update({
                u'current_item_count': current_item_count
            })

            response_formatter_object = ResponseFormatter({})
            response = response_formatter_object.format_delete_last_item_response(current_item_count,drink_desc)
            print('here!    ')
        elif(parameters['drink'] not in drinks_dict):
            response_formatter_object = ResponseFormatter(drinks_dict)
            response = response_formatter_object.format_cancel_item_not_exist()

        print("sending")
        print(response)
        return {'fulfillmentText':response}

    # Helper function tto handle deletion
    def cancel_item_intent_continue_helper(self,cancel_item_number,drinks_dict,doc_ref):
        deleted_item_stat = False
        deleted_item = ""
        for each_category in drinks_dict:
            category_drinks = drinks_dict[each_category]
            for each_item_num in category_drinks:
                if(each_item_num == cancel_item_number):
                    deleted_item_stat = True
                    deleted_item = category_drinks[each_item_num]['size'] + " " + each_category
                    len_dict = len(drinks_dict[each_category])
                    del drinks_dict[each_category][each_item_num]
                    if(len_dict==1):
                        del drinks_dict[each_category]
                    doc_ref.update({
                        u'drinks': drinks_dict
                    })
                    return deleted_item_stat,deleted_item
        return deleted_item_stat,deleted_item

    def cancel_item_intent_continue(self):

        print("cancel_item_intent_continue")
        print("--------------------------------------")


        user_id = self.request.userid
        parameters = self.request.parameters
        cancel_item_number = str(int(parameters.get('number')))

        document_exists = self.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = self.firestore_client.collection(u'current_order').document(user_id)
            drinks_dict = doc_ref.get().to_dict().get(u'drinks')

        print(drinks_dict)
        # to check if item_number present in order
        deleted_item_stat, deleted_item = self.cancel_item_intent_continue_helper(cancel_item_number,drinks_dict,doc_ref)

        response = 'Done, a ' + deleted_item + ' has been removed from your order. ' \
                                               'To continue with the order , say an item name ' \
                                               'or to complete your order, say "COMPLETE ORDER"'

        if not deleted_item_stat:
            response_formatter_object = ResponseFormatter(drinks_dict)
            response = response_formatter_object.format_cancel_item_not_exist()

        print(response)
        print(deleted_item_stat)
        print(deleted_item)

        return {'fulfillmentText': response}













