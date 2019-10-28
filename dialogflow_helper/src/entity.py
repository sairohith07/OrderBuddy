import dialogflow_v2 as dialogflow
from config import Config

class SEntity:

    def __init__(self):
        self.client = dialogflow.EntityTypesClient()

    def create(self, name, value_synonyms_map):
        entity_type = dialogflow.types.entity_type_pb2.EntityType()

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
        print(response)

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
