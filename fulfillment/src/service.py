from google.cloud import firestore

from factory import Factory
from response_formatter import ResponseFormatter
from config import Config
import copy


class Service:

    @staticmethod
    def default_welcome_intent(request):

        response = {
            'fulfillmentText': 'Hi ' + request.username + '. Welcome to Starbucks. What can i get you to drink?'
        }
        return response

    @staticmethod
    def sign_in_intent(request):
        response = {
            'fulfillmentText': 'Have a good day!'
        }
        return response

    @staticmethod
    def order_intent(request):

        user_id = request.userid
        parameters = request.parameters
        firestore_timestamp = firestore.SERVER_TIMESTAMP

        if ('drink' not in parameters) or (parameters['drink'] == ""):
            response = {'fulfillmentText': Config.order_intent_drink_check_fulfillment_text}
            return response
        if ('size' not in parameters) or (parameters['size'] == ""):
            response = {'fulfillmentText': Config.order_intent_size_check_fulfillment_text}
            return response
        if ('customize' not in parameters) or (parameters['customize'] == ""):
            response = {'fulfillmentText': Config.order_intent_size_check_fulfillment_text}
            return response

        # Assumption - Only one item per request.
        drink_name = parameters.get('drink')[0]
        drink_size = parameters.get('size')[0]
        drink_customization = parameters.get('customize')

        # INSERT TO DB (If collection not present, it get's created)
        document_exists = Factory.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = Factory.firestore_client.collection(u'current_order').document(user_id)
            doc_ref_dict = doc_ref.get().to_dict()

            current_item_count = doc_ref_dict.get(u'current_item_count')
            item_number = current_item_count + 1

            drinks_dict = doc_ref.get().to_dict().get(u'drinks')
            if drinks_dict is None:
                drinks_dict = {}

            if drink_name in drinks_dict:
                drinks_dict.get(drink_name)[str(item_number)] = {
                    u'size': drink_size,
                    u'customize': drink_customization
                }
            else:
                drinks_dict[drink_name] = {}
                drinks_dict[drink_name][str(item_number)] = {
                    u'size': drink_size,
                    u'customize': drink_customization
                }

            doc_ref.update({
                u'current_item_count': item_number,
                u'order_timestamp':firestore_timestamp,
                u'drinks': drinks_dict
            })

        else:
            current_item_count = 0
            item_number = current_item_count + 1
            doc_ref = Factory.firestore_client.collection(u'current_order').document(user_id)
            doc_ref.set({
                u'current_item_count': item_number,
                u'order_timestamp':firestore_timestamp,
                u'drinks': {
                    drink_name: {
                        str(item_number): {
                            u'size': drink_size,
                            u'customize': drink_customization
                        }
                    }
                }
            })
        response_text = 'Your order is updated with a ' + drink_size + ' ' + drink_name
        response_mid = "" if drink_customization[0].lower() == "no" else " With " + ','.join(drink_customization)
        response_tail = '. Do you want to add anything else?'
        response = {'fulfillmentText': response_text + response_mid + response_tail }

        return response

    @staticmethod
    def fallback_intent(request):
        ouput_contexts = request.output_contexts
        # Setting the lifeSpan of the whatever context that triggered fallback intent to 1
        if(len(ouput_contexts)>0):
            ouput_contexts[0]['lifespanCount'] = '1'
            print(ouput_contexts[0])
            response = {'outputContexts': ouput_contexts}
            return response



    @staticmethod
    def order_intent_no(request):
        response = None
        user_id = request.userid

        # Get the current order for the user
        doc_ref_current_order = Factory.firestore_client.collection(u'current_order').document(user_id)
        if doc_ref_current_order.get().exists:

            # create key  closed timestamp for the order
            doc_ref_current_order.update({u'closed_timestamp': firestore.SERVER_TIMESTAMP})
            doc_ref_dict = doc_ref_current_order.get().to_dict()

            # remove from current_order collection and move to history collection

            del doc_ref_dict[u'current_item_count']
            drinks_dict = doc_ref_current_order.get().to_dict().get(u'drinks')

            doc_ref_history = Factory.firestore_client.collection(u'history').document(user_id)
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
            response = {
                'fulfillmentText': 'Your order \n\n' + response_string + ' \n\n is confirmed.',
                "payload": {
                    "google": {
                        "expectUserResponse": True,
                        "systemIntent": {
                            "intent": "actions.intent.SIGN_IN",
                            "data": {
                                "@type": "type.googleapis.com/google.actions.v2.SignInValueSpec",
                                 "optContext": 'Your order \n\n' + response_string + ' \n\n is confirmed. \n\n' +
                                                'Would you like to sign in  help in personalization? \n \n For that '
                            }
                        }
                    }
                }
            }
        else:
            response = {'fulfillmentText': 'There is no existing order to place'}

        return response

    @staticmethod
    def cancel_order_intent_yes(request):
        user_id = request.userid
        doc_ref = Factory.firestore_client.collection(u'current_order').document(user_id)
        document_exists = doc_ref.get().exists
        if document_exists:
            doc_ref.delete()
        response = {'fulfillmentText': 'Your order  is cancelled.'}

        return response

    @staticmethod
    def complete_order_intent(request):
        response = None
        user_id = request.userid
        doc_ref = Factory.firestore_client.collection(u'current_order').document(user_id)
        document_exists = doc_ref.get().exists
        drinks_dict = None
        if(document_exists):
            drinks_dict = doc_ref.get().to_dict().get(u'drinks')

        if document_exists and drinks_dict is not None and len(drinks_dict)>0 :
            response = {'fulfillmentText': 'Are you sure you want to place the order?'}
        else:
            response_formatter_object = ResponseFormatter({})
            response = {'fulfillmentText': response_formatter_object.format_empty_cart_response()}
        return response

    @staticmethod
    def complete_order_intent_yes(request):
        return Service.order_intent_no(request)

    @staticmethod
    def cancel_item_intent(request):
        user_id = request.userid
        parameters = request.parameters

        print(parameters)

        doc_ref = Factory.firestore_client.collection(u'current_order').document(user_id)

        # No document check
        if not doc_ref.get().exists:
            response_formatter_object = ResponseFormatter({})
            response = {'fulfillmentText': response_formatter_object.format_empty_cart_response()}
            return response

        doc_ref_dict = doc_ref.get().to_dict()
        drinks_dict = doc_ref_dict.get(u'drinks')
        current_item_count = doc_ref_dict.get(u'current_item_count')

        #Empty document check
        if(drinks_dict is None or len(drinks_dict)==0):
            response_formatter_object = ResponseFormatter({})
            response = {'fulfillmentText': response_formatter_object.format_empty_cart_response()}
            return response

        #  drink in current utterance --- drink has been ordered-------------- there is atleast one of this drinks-----
        if(len(parameters['drink'])>0 and (parameters['drink'] in drinks_dict and len(drinks_dict[parameters['drink']])>0)):
            drinks_dict_copy = copy.deepcopy(drinks_dict[parameters['drink']])
            if (len(parameters['size'])) > 0:
                for item_number in drinks_dict[parameters['drink']].keys():
                    drink_params_dict = drinks_dict[parameters['drink']][item_number]
                    if drink_params_dict['size'] != parameters['size']:
                        del drinks_dict_copy[item_number]

                response_formatter_object = ResponseFormatter({parameters['drink']: drinks_dict_copy})
                response = response_formatter_object.format_cancel_intent_response()

            else:
                response_formatter_object = ResponseFormatter({parameters['drink']: drinks_dict[parameters['drink']]})
                response = response_formatter_object.format_cancel_intent_response()

        # drinks in present in utterance but no drink of that category of that order
        elif ( (len(parameters['drink']) > 0) and  (parameters['drink'] not in drinks_dict) ):
            response_formatter_object = ResponseFormatter(drinks_dict)
            response = response_formatter_object.format_cancel_item_not_exist()

        elif( len(parameters['drink']) == 0):
            drink_desc = ""
            last_item_stat = False
            for each_category in drinks_dict:
                drinks_in_category = drinks_dict[each_category]
                for each_item_num in drinks_in_category:
                    if(each_item_num == current_item_count):
                        customize_text = ','.join(drinks_in_category[each_item_num]['customize'])
                        drink_desc += drinks_in_category[each_item_num]['size']+\
                                      " " + each_category + ("" if customize_text.lower()=="no" else " With "+customize_text )
                        last_item_stat = True

            if not last_item_stat:
                current_item_count = 1
                for each_category in drinks_dict:
                    drinks_in_category = drinks_dict[each_category]
                    for each_item_num in drinks_in_category:
                        if(int(each_item_num))>current_item_count:
                            current_item_count = int(each_item_num)
                            customize_text = ','.join(drinks_in_category[each_item_num]['customize'])
                            drink_desc = drinks_in_category[each_item_num]['size'] + \
                                         " " + each_category + ("" if customize_text.lower()=="no" else " With "+customize_text )

            doc_ref.update({
                u'current_item_count': current_item_count
            })

            response_formatter_object = ResponseFormatter({})
            response = response_formatter_object.format_delete_last_item_response(current_item_count,drink_desc)
            print('here!    ')


        print("sending")
        print(response)
        return {'fulfillmentText':response}

    # Helper function tto handle deletion
    @staticmethod
    def cancel_item_intent_continue_helper(cancel_item_number,drinks_dict,doc_ref):
        deleted_item_stat = False
        deleted_item = ""
        for each_category in drinks_dict:
            category_drinks = drinks_dict[each_category]
            for each_item_num in category_drinks:
                if(each_item_num == cancel_item_number):
                    deleted_item_stat = True
                    customize_text = ','.join(category_drinks[each_item_num]['customize'])
                    deleted_item = category_drinks[each_item_num]['size'] + \
                                   " " + each_category + ("" if customize_text.lower()=="no" else " With "+customize_text)
                    len_dict = len(drinks_dict[each_category])
                    del drinks_dict[each_category][each_item_num]
                    if(len_dict==1):
                        del drinks_dict[each_category]
                    doc_ref.update({
                        u'drinks': drinks_dict
                    })
                    return deleted_item_stat,deleted_item
        return deleted_item_stat,deleted_item

    def adjust_last_added_item_id(request):
        user_id = request.userid
        # Get the current order for the user
        doc_ref_current_order = Factory.firestore_client.collection(u'current_order').document(user_id)
        if doc_ref_current_order.get().exists:
            last_added_item_id = doc_ref_current_order.get().to_dict().get(u'current_item_count')
            drinks_dict = doc_ref_current_order.get().to_dict().get(u'drinks')
            id_max = 0
            for each_category in drinks_dict:
                category_drinks = drinks_dict[each_category]
                for each_item_num in category_drinks:
                    if(id_max < int(each_item_num) ):
                        id_max = int(each_item_num)
            if(int(last_added_item_id) > id_max):
                doc_ref_current_order.update({
                    u'current_item_count': id_max
                })

    @staticmethod
    def cancel_item_intent_continue(request):

        print("cancel_item_intent_continue")
        print("--------------------------------------")


        user_id = request.userid
        parameters = request.parameters
        cancel_item_number = str(int(parameters.get('number')))

        document_exists = Factory.firestore_client.collection(u'current_order').document(user_id).get().exists
        if document_exists:
            doc_ref = Factory.firestore_client.collection(u'current_order').document(user_id)
            drinks_dict = doc_ref.get().to_dict().get(u'drinks')

        print(drinks_dict)
        # to check if item_number present in order
        deleted_item_stat, deleted_item = Service.cancel_item_intent_continue_helper(cancel_item_number,drinks_dict,doc_ref)

        response = 'Done, a ' + deleted_item + ' has been removed from your order. ' \
                                               'To continue with the order , say an item name ' \
                                               'or to complete your order, say "COMPLETE ORDER"'

        Service.adjust_last_added_item_id(request)

        if not deleted_item_stat:
            response_formatter_object = ResponseFormatter(drinks_dict)
            response = response_formatter_object.format_cancel_item_not_exist()
            return {'fulfillmentText': response}

        print(response)
        print(deleted_item_stat)
        print(deleted_item)

        return {'fulfillmentText': response}









