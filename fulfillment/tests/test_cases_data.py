class TestCasesData:

    # Drink name is not present
    test_order_intent_drink_null = {
        "queryResult": {
            "queryText": "I want to order",
            "parameters": {
            },
            "intent": {
                "name": "projects/order-buddy-257400/agent/intents/aa60da0d-c87f-4a2e-9a08-cdffa419b94f",
                "displayName": "order_intent"
            }
        }
    }

    # Drink is empty
        # when drink is not a compulsory parameter, the key will be a empty streing ""
        # when drink is present, it will always come as a list
    test_order_intent_drink_empty = {
        "queryResult": {
            "queryText": "I want to order",
            "parameters": {
                "drink": ""
            },
            "intent": {
                "name": "projects/order-buddy-257400/agent/intents/aa60da0d-c87f-4a2e-9a08-cdffa419b94f",
                "displayName": "order_intent"
            }
        }
    }

    # Drink name is present but size is not present
    test_order_intent_size_null = {
        "queryResult": {
            "queryText": "I want a Cafe Latte",
            "parameters": {
                "drink": ['CAFFE LATTE']
            },
            "intent": {
                "name": "projects/order-buddy-257400/agent/intents/aa60da0d-c87f-4a2e-9a08-cdffa419b94f",
                "displayName": "order_intent"
            }
        }
    }

    # Drink name is present but size is empty
    test_order_intent_size_empty = {
        "queryResult": {
            "queryText": "I want a Cafe Latte",
            "parameters": {
                "drink": ['CAFFE LATTE'],
                "size": ""
            },
            "intent": {
                "name": "projects/order-buddy-257400/agent/intents/aa60da0d-c87f-4a2e-9a08-cdffa419b94f",
                "displayName": "order_intent"
            }
        }
    }



    # Try to complete an order with no document in firestore
    # Expects a response conveying a empty cart
    # Deletes the existing document

    clear_document_cancel_order = {
        "queryResult": {
            "queryText": "Exit",
            "parameters": {},
            "intent": {
              "name": "projects/orderbuddy/agent/intents/8c7896fb-d807-4176-be2f-d663ca057079",
              "displayName": "cancel_order_intent"
            }
        }
    }
    clear_document_cancel_order_yes_followup = {
        "queryResult": {
            "queryText": "Yes",
            "parameters": {},
            "intent": {
              "name": "projects/orderbuddy/agent/intents/a87ca1b6-1ad0-4dc9-9d1b-c13b81f0cb8b",
              "displayName": "cancel_order_intent.yes"
            }
        }
    }

    test_complete_order_intent_null_document = {
        "queryResult": {
            "queryText": "Place Order",
            "parameters": {},
            "intent": {
              "name": "projects/orderbuddy/agent/intents/6620c32d-2e78-488a-9e85-c9ac02a4d386",
              "displayName": "complete_order_intent"
            }
        }
    }

    test_cancel_item_intent_null_document = {
        "queryResult": {
            "queryText": "Cancel",
            "parameters": {},
            "intent": {
              "name": "projects/delete-this-2-xiocsx/agent/intents/aa60da0d-c87f-4a2e-9a08-cdffa419b94f",
              "displayName": "cancel_item_intent"
            }
        }
    }

