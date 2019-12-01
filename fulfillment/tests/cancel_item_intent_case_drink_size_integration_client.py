import dialogflow_v2 as dialogflow
from config import Config
from google.protobuf import json_format
from entity import SEntity
from test_cases_data import TestCasesData
import time

class CancelIntentCaseDrinkSizeIntegration:


    @staticmethod
    def google_client_session():
        client = dialogflow.SessionsClient()
        session = client.session_path(Config.GOOGLE_PROJECT_ID, Config.SESSION_ID)
        return client, session

    @staticmethod
    def get_test_detect_intent_entity_drink_size_for_text():
        intent = 'cancel_item_intent'
        test_tuples = []
        sentity = SEntity()
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
        return test_tuples

    @staticmethod
    def write_to_error_file(output_file, i, j, training_phrase, golden_intent, golden_drink, golden_size,
                            drink_potential, size_potential, training_phrase_potential, extracted_intent,
                            extracted_drink, extracted_size, test_status):
        output_file.write('#########: {}, {} \n'.format(i, j))
        output_file.write(
            "Training Phrase: {} \nGolden Intent: {} \nGolden Drink: {} \nGolden Size: {} \nDrink Potential: {} \nSize Potential: {} \n"
            .format(training_phrase, golden_intent, golden_drink, golden_size, drink_potential, size_potential))
        output_file.write('"Training Phrase Potential: {} \n'.format(training_phrase_potential))
        output_file.write('>>> Result: {} \n')
        output_file.write('Test Status: {} \n'.format(test_status))
        output_file.write('"Extracted Intent: {} \nExtracted Drink: {} \nExtracted Size: {} \n'.format(extracted_intent, extracted_drink, extracted_size))

    @staticmethod
    def test_detect_intent_entity_drink_size_for_text():

        output_file = open('../output/cancel_item_intent_drink_size_integration_output.txt', 'w')
        intent_error_file = open('../output/cancel_item_intent_drink_size_integration_intent_error.txt', 'w')
        drink_error_file = open('../output/cancel_item_intent_drink_size_integration_drink_error.txt', 'w')
        size_error_file = open('../output/cancel_item_intent_drink_size_integration_size_error.txt', 'w')

        client = dialogflow.SessionsClient()
        session = client.session_path(Config.GOOGLE_PROJECT_ID, Config.SESSION_ID)
        test_tuples = CancelIntentCaseDrinkSizeIntegration.get_test_detect_intent_entity_drink_size_for_text()

        print("Test tuples count: {} \n".format(len(test_tuples)))
        output_file.write("Test tuples count: {} \n".format(len(test_tuples)))

        print("Training phrases count: {} \n".format(len(TestCasesData.cancel_item_case_drink_size_input_test_phrases)))
        output_file.write("Training phrases count: {} \n".format(len(TestCasesData.cancel_item_case_drink_size_input_test_phrases)))

        total_so_far = 0
        correct_so_far=0

        for i in range(len(TestCasesData.cancel_item_case_drink_size_input_test_phrases)):
            training_phrase = TestCasesData.cancel_item_case_drink_size_input_test_phrases[i]
            for j in range(len(test_tuples)):
                total_so_far += 1
                test_data = test_tuples[j]
                golden_intent = test_data[0]
                golden_drink = test_data[1]
                golden_size = test_data[2]
                drink_potential = test_data[3]
                size_potential = test_data[4]

                print('#########: {}, {}'.format(i, j))
                print(training_phrase)
                print(golden_intent, golden_drink, golden_size, drink_potential, size_potential)
                output_file.write('#########: {}, {} \n'.format(i, j))
                output_file.write("Training Phrase: {} \nGolden Intent: {} \nGolden Drink: {} \nGolden Size: {} \n"
                                  "Drink Potential: {} \nSize Potential: {} \n"
                                  .format(training_phrase, golden_intent, golden_drink, golden_size, drink_potential,
                                          size_potential))

                # Replace the drink and the size
                training_phrase_potential = training_phrase.replace('{drink}', drink_potential)
                training_phrase_potential = training_phrase_potential.replace('{size}', size_potential)
                print(training_phrase_potential)
                output_file.write('"Training Phrase Potential: {} \n'.format(training_phrase_potential))

                text_input = dialogflow.types.TextInput(text=training_phrase_potential, language_code='en-US')
                query_input = dialogflow.types.QueryInput(text=text_input)
                response = client.detect_intent(session, query_input)
                extracted_intent = response.query_result.intent.display_name
                parameters = json_format.MessageToDict(response.query_result.parameters)
                extracted_drink = " " if ("drink" not in parameters) else parameters['drink']
                extracted_size = " " if ("size" not in parameters) else parameters['size']

                # Intent and Parameters check
                test_status = True
                if  extracted_intent != golden_intent:
                    test_status = False
                    CancelIntentCaseDrinkSizeIntegration.write_to_error_file(intent_error_file, i, j, training_phrase,
                                                                     golden_intent, golden_drink, golden_size,
                                                                     drink_potential, size_potential,
                                                                     training_phrase_potential, extracted_intent,
                                                                     extracted_drink, extracted_size, test_status)
                if extracted_drink != golden_drink:
                    test_status = False
                    CancelIntentCaseDrinkSizeIntegration.write_to_error_file(drink_error_file, i, j, training_phrase,
                                                                     golden_intent, golden_drink, golden_size,
                                                                     drink_potential, size_potential,
                                                                     training_phrase_potential, extracted_intent,
                                                                     extracted_drink, extracted_size, test_status)
                if extracted_size != golden_size:
                    test_status = False
                    CancelIntentCaseDrinkSizeIntegration.write_to_error_file(size_error_file, i, j, training_phrase,
                                                                     golden_intent, golden_drink, golden_size,
                                                                     drink_potential, size_potential,
                                                                     training_phrase_potential, extracted_intent,
                                                                     extracted_drink, extracted_size, test_status)

                correct_so_far += 0 if test_status is False else 1
                output_file.write('>>> Result: {} \n')
                output_file.write('Test Status: {} \n'.format(test_status))
                output_file.write('Extracted Intent: {} \nExtracted Drink: {} \nExtracted Size: {} \n'
                                  .format(extracted_intent, extracted_drink, extracted_size))

                # Sleep to avoid resource exhaustion
                time.sleep(0.5)
                print('Accuracy so far: {} \n Total Phrases: {} \n Correctly Predicted: {} \n'
                      .format((correct_so_far/total_so_far),total_so_far,correct_so_far))

        output_file.close()
        intent_error_file.close()
        drink_error_file.close()
        size_error_file.close()

CancelIntentCaseDrinkSizeIntegration.test_detect_intent_entity_drink_size_for_text()