import json

class Certificates:

    @staticmethod
    def get(filepath='../input/certs.json'):
        with open(filepath) as json_file:
            certs_dict = json.load(json_file)
        return certs_dict

print(Certificates.get())