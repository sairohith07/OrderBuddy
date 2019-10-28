import dialogflow_v2 as dialogflow
from config import Config

class SAgent:
    def __init__(self):
        self.client = dialogflow.AgentsClient()