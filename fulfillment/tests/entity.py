import dialogflow_v2 as dialogflow
from config import Config
from test_cases_data import TestCasesData


class SEntity:

    def __init__(self):
        self.client = dialogflow.EntityTypesClient()

    def create(self, name, value_synonyms_map, enable_fuzzy_extraction=False):
        entity_type = dialogflow.types.entity_type_pb2.EntityType()
        entity_type.enable_fuzzy_extraction = enable_fuzzy_extraction

        entity_list = []
        # Create Entities
        for value, synonyms in value_synonyms_map.items():
            entity = entity_type.Entity()
            entity.value = value
            entity.synonyms.extend(synonyms)
            entity_list.append(entity)

        entity_type = {
            'display_name': name,
            'kind': 'KIND_MAP',
            'entities': entity_list
        }
        parent = self.client.project_agent_path(Config.GOOGLE_PROJECT_ID)
        response = self.client.create_entity_type(parent, entity_type)
        return response

    def get(self, entity_type_id):
        entity_type_dict = {}
        name = self.client.entity_type_path(Config.GOOGLE_PROJECT_ID, entity_type_id)
        response = self.client.get_entity_type(name)
        entity_dict = {}
        for entity in response.entities:
            entity_dict[entity.value] = entity.synonyms
        entity_type_dict[response.display_name] = {
            'name': response.name[response.name.rfind('/') + 1:],
            'kind': response.kind,
            'entity': entity_dict
        }
        return entity_type_dict

    def list(self):
        entity_type_dict = {}
        parent = self.client.project_agent_path(Config.GOOGLE_PROJECT_ID)
        # Iterate over all results
        for page in self.client.list_entity_types(parent).pages:
            for element in page:
                entity_type_dict[element.display_name] = element.name[element.name.rfind('/')+1: ]
                # for entity in element.entities:
                #     print(entity.value, entity.synonyms)
        return entity_type_dict

# sentity = SEntity()
# entity_list = sentity.list()
# drink_entity_id = entity_list['drink']
# drinks = sentity.get(drink_entity_id)['drink']['entity']
# size_entity_id = entity_list['size']
# sizes = sentity.get(size_entity_id)['size']['entity']
# for drink in  drinks:
#     drink_synonyms = drinks[drink]
#     for size in sizes:
#         size_synonyms = sizes[size]
#         for drink_synonym in drink_synonyms:
#             for size_synonym in size_synonyms:
#                 print(drink, size, drink_synonym, size_synonym)
#                 for training_phrase in TestCasesData.order_intent_drink_size_training_phrases:
#                     # Replace the drink and the size
#                     training_phrase = training_phrase.replace('{drink}', drink_synonym)
#                     training_phrase = training_phrase.replace('{size}', size_synonym)
#
# print(drinks)
# print(sizes)