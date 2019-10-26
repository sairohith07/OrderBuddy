import dialogflow_v2 as dialogflow




def list_intents(project_id):
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)

    intents = intents_client.list_intents(parent)

    for intent in intents:
        print('=' * 20)
        print('Intent name: {}'.format(intent.name))
        print('Intent display_name: {}'.format(intent.display_name))
        print('Action: {}\n'.format(intent.action))
        print('Root followup intent: {}'.format(
            intent.root_followup_intent_name))
        print('Parent followup intent: {}\n'.format(
            intent.parent_followup_intent_name))

        print('Input contexts:')
        for input_context_name in intent.input_context_names:
            print('\tName: {}'.format(input_context_name))

        print('Output contexts:')
        for output_context in intent.output_contexts:
            print('\tName: {}'.format(output_context.name))

def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))

GOOGLE_PROJECT_ID = "delete-this-vjdftp"
session_id = "abc-123"
context_short_name = "does_not_matter"

context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + \
               context_short_name.lower()
intents_client = dialogflow.IntentsClient()


display_name = "apples"
training_phrases_parts = {"I like apples","apples are my life"}
message_texts = {"shut up!"}
# create_intent(GOOGLE_PROJECT_ID,display_name,training_phrases_parts,message_texts)

list_intents(GOOGLE_PROJECT_ID)