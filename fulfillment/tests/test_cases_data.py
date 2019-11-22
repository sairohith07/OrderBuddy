class TestCasesData:

    # Drink name is not present
    test_order_intent_drink_null = {
        "queryResult": {
            "queryText": "I want to cancel this item",
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
            "queryText": "I want to cancel this item",
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
            "queryText": "I want to cancel this item",
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
            "queryText": "I want to cancel this item",
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