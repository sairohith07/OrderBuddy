import dialogflow_v2 as dialogflow
from config import Config
import pytest
from google.protobuf import json_format
from entity import SEntity
from test_cases_data import TestCasesData
import time

class TestOrderIntentClient:

    @pytest.fixture(scope="module")
    def google_client_session(self):
        client = dialogflow.SessionsClient()
        session = client.session_path(Config.GOOGLE_PROJECT_ID, Config.SESSION_ID)
        return client, session

    @pytest.fixture(scope="module")
    def google_entity_client(self):
        sentity = SEntity()
        return sentity

    @pytest.fixture
    def get_test_detect_intent_entity_drink_for_text(self, google_entity_client):
        intent = 'order_intent'
        test_tuples = []
        sentity = google_entity_client
        entity_list = sentity.list()
        drink_entity_id = entity_list['drink']
        drinks = sentity.get(drink_entity_id)['drink']['entity']
        size_entity_id = entity_list['size']
        sizes = sentity.get(size_entity_id)['size']['entity']
        for drink in drinks:
            drink_synonyms = drinks[drink]
            for size in sizes:
                size_synonyms = sizes[size]
                for drink_synonym in drink_synonyms:
                    for size_synonym in size_synonyms:
                        test_tuples.append((intent, drink, size, drink_synonym, size_synonym))
        print("Test tuples count: {}".format(len(test_tuples)))
        return test_tuples

    def test_detect_intent_entity_drink_for_text(self, google_client_session, get_test_detect_intent_entity_drink_for_text):
        client, session = google_client_session
        print("Test tuples count: {}".format(len(TestCasesData.order_intent_drink_size_training_phrases)))
        i = 0
        for training_phrase in TestCasesData.order_intent_drink_size_training_phrases:
            for test_data in get_test_detect_intent_entity_drink_for_text:
                golden_intent = test_data[0]
                golden_drink = test_data[1]
                golden_size = test_data[2]
                drink_potential = test_data[3]
                size_potential = test_data[4]

                print('#########: {}'.format(i))
                print(training_phrase)
                print(golden_intent, golden_drink, golden_size, drink_potential, size_potential)

                # Replace the drink and the size
                training_phrase_potential = training_phrase.replace('{drink}', drink_potential)
                training_phrase_potential = training_phrase_potential.replace('{size}', size_potential)
                print(training_phrase_potential)

                if drink_potential == 'WHITE CHOCOLATE MOCHA':
                    continue
                elif drink_potential == 'HORCHATA ALMOND MILK':
                    continue
                elif training_phrase_potential == "I'd like to order a big WHITE CHOCOLATE MOCHA":
                    continue
                elif training_phrase_potential == "I'd like to order a huge WHITE CHOCOLATE MOCHA":
                    continue

                text_input = dialogflow.types.TextInput(text=training_phrase_potential, language_code='en-US')
                query_input = dialogflow.types.QueryInput(text=text_input)
                response = client.detect_intent(session, query_input)
                parameters = json_format.MessageToDict(response.query_result.parameters)

                print(parameters)

                # Intent Check
                assert response.query_result.intent.display_name == golden_intent
                assert parameters['drink'][0] == golden_drink
                assert parameters['size'][0] == golden_size

                time.sleep(5)
                i = i + 1

# sclient = SClient()
# sclient.detect_intent_for_text('My favorite is Tossed Salad')
