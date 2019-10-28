from entity import SEntity
from intent import SIntent
from client import SClient

# Entity
# sentity = SEntity()
# value_synonym_map = {
#     "a": ["a", "aa", "aaa"],
#     "b": ["c"]
# }
# # sentity.create("B", value_synonym_map)
# result = sentity.list()
# print(result)
#
# print(sentity.get(result['dish']))

# Intent
# GOOGLE_PROJECT_ID = "dish-sentiment-analysis"
# session_id = "abc-123"
# context_short_name = "does_not_matter"
#
# context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + context_short_name.lower()
# intents_client = dialogflow.IntentsClient()

# sintent = SIntent()
# display_name = "apples"
# training_phrases_parts = {"I like apples","apples are my life"}
# message_texts = {"shut up!"}
# sintent.create_intent(display_name, training_phrases_parts, message_texts)
#
# sintent.list_intents()

sclient = SClient()
sclient.detect_intent_for_text('My favorite fruit is apple')



