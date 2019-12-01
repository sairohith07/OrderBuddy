import dialogflow_v2 as dialogflow
from config import Config
from google.protobuf import json_format
from entity import SEntity
from test_cases_data import TestCasesData
import time


class CustomizeIntentIntegrationClient:

    @staticmethod
    def google_client_session():
        client = dialogflow.SessionsClient()
        session = client.session_path(Config.GOOGLE_PROJECT_ID, Config.SESSION_ID)
        return client, session

    @staticmethod
    def get_test_detect_customization_entity_drink_size_customize_for_text():
        intent = 'order_intent'
        test_tuples = []
        sentity = SEntity()
        entity_list = sentity.list()
        drink_entity_id = entity_list['drink']
        drinks = sentity.get(drink_entity_id)['drink']['entity']
        size_entity_id = entity_list['size']
        sizes = sentity.get(size_entity_id)['size']['entity']
        customize_entity_id = entity_list['customization']
        customizations = sentity.get(customize_entity_id)['customization']['entity']
        for drink in drinks:
            drink_synonyms = drinks[drink]
            for size in sizes:
                size_synonyms = sizes[size]
                for customize in customizations:
                    customize_synonyms = customizations[customize]
                    for drink_synonym in drink_synonyms:
                        for size_synonym in size_synonyms:
                            for customize_synonym in customize_synonyms:
                                test_tuples.append((intent, drink, size, customize,
                                                    drink_synonym, size_synonym, customize_synonym))
        return test_tuples

    @staticmethod
    def write_to_error_file(output_file, i, j, training_phrase, golden_intent, golden_drink, golden_size,
                            golden_customization, drink_potential, size_potential, customize_potential,
                            training_phrase_potential, extracted_intent, extracted_drink, extracted_size,
                            extracted_customization, test_status):
        output_file.write('#########: {}, {} \n'.format(i, j))
        output_file.write(
            "Training Phrase: {} \nGolden Intent: {} \nGolden Drink: {} \nGolden Size: {} \nGolden Customization: {}"
            "\nDrink Potential: {} \nSize Potential: {} \n Customize potential: {} \n"
            .format(training_phrase, golden_intent, golden_drink, golden_size, golden_customization,
                    drink_potential, size_potential, customize_potential))
        output_file.write('"Training Phrase Potential: {} \n'.format(training_phrase_potential))
        output_file.write('>>> Result: {} \n')
        output_file.write('Test Status: {} \n'.format(test_status))
        output_file.write('Extracted Intent: {} \nExtracted Drink: {} \nExtracted Size: {} '
                          '\nExtracted Customization: {} \n'
                          .format(extracted_intent, extracted_drink, extracted_size, extracted_customization))

    @staticmethod
    def test_detect_customization_entity_drink_size_customize_for_text():

        output_file = open('../output/customize_intent_drink_size_customize_integration_output.txt', 'w')
        intent_error_file = open('../output/customize_intent_drink_size_customize_integration_intent_error.txt', 'w')
        drink_error_file = open('../output/customize_intent_drink_size_customize_integration_drink_error.txt', 'w')
        size_error_file = open('../output/customize_intent_drink_size_customize_integration_size_error.txt', 'w')
        customize_error_file = open('../output/customize_intent_drink_size_customize_integration_customize_error.txt', 'w')

        total_count = 0
        intent_error_count = 0
        drink_error_count = 0
        size_error_count = 0
        customize_error_count = 0

        client = dialogflow.SessionsClient()
        session = client.session_path(Config.GOOGLE_PROJECT_ID, Config.SESSION_ID)
        test_tuples = CustomizeIntentIntegrationClient\
            .get_test_detect_customization_entity_drink_size_customize_for_text()

        print("Test tuples count: {} \n".format(len(test_tuples)))
        output_file.write("Test tuples count: {} \n".format(len(test_tuples)))

        print("Training phrases count: {} \n".format(len(TestCasesData
                                                         .order_intent_drink_size_customize_training_phrases)))
        output_file.write("Training phrases count: {} \n"
                          .format(len(TestCasesData.order_intent_drink_size_customize_training_phrases)))

        for i in range(len(TestCasesData.order_intent_drink_size_customize_training_phrases)):
            training_phrase = TestCasesData.order_intent_drink_size_customize_training_phrases[i]
            for j in range(len(test_tuples)):
                test_data = test_tuples[j]
                golden_intent = test_data[0]
                golden_drink = test_data[1]
                golden_size = test_data[2]
                golden_customization = test_data[3]
                drink_potential = test_data[4]
                size_potential = test_data[5]
                customize_potential = test_data[6]

                print('#########: {}, {}'.format(i, j))
                print(training_phrase)
                print(golden_intent, golden_drink, golden_size, golden_customization,
                      drink_potential, size_potential, customize_potential)
                output_file.write('#########: {}, {} \n'.format(i, j))
                output_file.write("Training Phrase: {} \nGolden Intent: {} \nGolden Drink: {} \nGolden Size: {} "
                                  "\nGolden customization: {} \nDrink Potential: {} \nSize Potential: {} "
                                  "\n Customize Potential: {} \n"
                                  .format(training_phrase, golden_intent, golden_drink, golden_size,
                                          golden_customization, drink_potential, size_potential, customize_potential))

                # Replace the drink and the size
                training_phrase_potential = training_phrase.replace('{drink}', drink_potential)
                training_phrase_potential = training_phrase_potential.replace('{size}', size_potential)
                training_phrase_potential = training_phrase_potential.replace('{customize}', customize_potential)
                print(training_phrase_potential)
                output_file.write('"Training Phrase Potential: {} \n'.format(training_phrase_potential))

                text_input = dialogflow.types.TextInput(text=training_phrase_potential, language_code='en-US')
                query_input = dialogflow.types.QueryInput(text=text_input)
                response = client.detect_intent(session, query_input)
                extracted_intent = response.query_result.intent.display_name
                parameters = json_format.MessageToDict(response.query_result.parameters)

                extracted_drink = 'EMPTY'
                if 'drink' in parameters.keys():
                    if parameters['drink']:
                        extracted_drink = parameters['drink'][0]

                extracted_size = 'EMPTY'
                if 'size' in parameters.keys():
                    if parameters['size']:
                        extracted_size = parameters['size'][0]

                extracted_customization = 'EMPTY'
                if 'customize' in parameters.keys():
                    if parameters['customize']:
                        extracted_customization = parameters['customize'][0]

                # Intent and Parameters check
                test_status = True
                if extracted_intent != golden_intent:
                    test_status = False
                    intent_error_count = intent_error_count + 1
                    CustomizeIntentIntegrationClient.write_to_error_file(intent_error_file, i, j, training_phrase,
                                                                         golden_intent, golden_drink, golden_size,
                                                                         golden_customization, drink_potential,
                                                                         size_potential, customize_potential,
                                                                         training_phrase_potential, extracted_intent,
                                                                         extracted_drink, extracted_size,
                                                                         extracted_customization, test_status)
                if extracted_drink != golden_drink:
                    test_status = False
                    drink_error_count = drink_error_count + 1
                    CustomizeIntentIntegrationClient.write_to_error_file(drink_error_file, i, j, training_phrase,
                                                                         golden_intent, golden_drink, golden_size,
                                                                         golden_customization, drink_potential,
                                                                         size_potential, customize_potential,
                                                                         training_phrase_potential, extracted_intent,
                                                                         extracted_drink, extracted_size,
                                                                         extracted_customization, test_status)
                if extracted_size != golden_size:
                    test_status = False
                    size_error_count = size_error_count + 1
                    CustomizeIntentIntegrationClient.write_to_error_file(size_error_file, i, j, training_phrase,
                                                                         golden_intent, golden_drink, golden_size,
                                                                         golden_customization, drink_potential,
                                                                         size_potential, customize_potential,
                                                                         training_phrase_potential, extracted_intent,
                                                                         extracted_drink, extracted_size,
                                                                         extracted_customization, test_status)
                print('extracted_customization!!!: ', extracted_customization)

                if extracted_customization != golden_customization:
                    test_status = False
                    customize_error_count = customize_error_count + 1
                    CustomizeIntentIntegrationClient.write_to_error_file(customize_error_file, i, j, training_phrase,
                                                                         golden_intent, golden_drink, golden_size,
                                                                         golden_customization, drink_potential,
                                                                         size_potential, customize_potential,
                                                                         training_phrase_potential, extracted_intent,
                                                                         extracted_drink, extracted_size,
                                                                         extracted_customization, test_status)

                output_file.write('>>> Result: {} \n')
                output_file.write('Test Status: {} \n'.format(test_status))
                output_file.write('Extracted Intent: {} \nExtracted Drink: {} \nExtracted Size: {} '
                                  '\nExtracted Customization: {} \n'
                                  .format(extracted_intent, extracted_drink, extracted_size, extracted_customization))

                # Sleep to avoid resource exhaustion
                time.sleep(0.5)
                total_count = total_count + 1
                if total_count == 1000:
                    break
            if total_count == 1000:
                break

        output_file.write('######## \nTotal Count: {} \nIntent Error count: {} \nDrink Error Count: {} '
                          '\nSize Error Count: {} \nCustomize Error Count: {}'
                          .format(total_count, intent_error_count, drink_error_count, size_error_count,
                                  customize_error_count))
        intent_error_file.write('######## \nIntent Error count: {} \n'.format(intent_error_count))
        drink_error_file.write('######## \nDrink Error count: {} \n'.format(drink_error_count))
        size_error_file.write('######## \nSize Error count: {} \n'.format(size_error_count))
        customize_error_file.write('######## \nCustomize Error count: {} \n'.format(customize_error_count))

        output_file.close()
        intent_error_file.close()
        drink_error_file.close()
        size_error_file.close()
        customize_error_file.close()


CustomizeIntentIntegrationClient.test_detect_customization_entity_drink_size_customize_for_text()
