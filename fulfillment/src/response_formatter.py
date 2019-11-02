class ReponseFormatter:

    def __init__(self, response_dict):
        self.response_dict = response_dict

    def format(self):
        response_string = ""
        for item_name in self.response_dict.keys():
            drink_name_dict = self.response_dict[item_name]
            for item_number in drink_name_dict.keys():
                response_string = response_string + item_number+ ": " + item_name + ", with size " + drink_name_dict[item_number]['size'] + "\n\n"

        return response_string