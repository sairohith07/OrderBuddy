import dialogflow_v2 as dialogflow
from config import Config

class SIntent:
    def __init__(self):
        self.client = dialogflow.IntentsClient()

    def create_intent(self, display_name, training_sentences, message_texts):
        parent = self.client.project_agent_path(Config.GOOGLE_PROJECT_ID)

        # Training Phrases
        training_phrases = []
        for training_sentence in training_sentences:
            part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_sentence)
            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        # Response Text
        text = dialogflow.types.Intent.Message.Text(text=message_texts)
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message])

        response = self.client.create_intent(parent, intent)
        print('Intent created: {}'.format(response))

    def list_intents(self):
        parent = self.client.project_agent_path(Config.GOOGLE_PROJECT_ID)
        intents = self.client.list_intents(parent)

        for intent in intents:
            print('=' * 20)
            print(intent)
            # print('Intent name: {}'.format(intent.name))
            # print('Intent display_name: {}'.format(intent.display_name))
            # print('Action: {}\n'.format(intent.action))
            # print('Root followup intent: {}'.format(
            #     intent.root_followup_intent_name))
            # print('Parent followup intent: {}\n'.format(
            #     intent.parent_followup_intent_name))
            #
            # print('Input contexts:')
            # for input_context_name in intent.input_context_names:
            #     print('\tName: {}'.format(input_context_name))
            #
            # print('Output contexts:')
            # for output_context in intent.output_contexts:
            #     print('\tName: {}'.format(output_context.name))