import dialogflow_v2 as dialogflow
from config import Config

class SClient:
    def __init__(self):
        self.client = dialogflow.SessionsClient()

    def detect_intent_for_text(self, text):
        session = self.client.session_path(Config.GOOGLE_PROJECT_ID, Config.SESSION_ID)
        # TODO: Initialize `query_input`:
        text_input = dialogflow.types.TextInput(text=text, language_code='en-US')
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = self.client.detect_intent(session, query_input)
        print(response)

