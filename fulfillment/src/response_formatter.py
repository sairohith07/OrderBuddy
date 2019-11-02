from collections import Counter


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

    def format_complete_order(self):
        response_string = ""
        order = Counter()
        for drink in list(self.response_dict.keys()):
            for size in list(self.response_dict[drink].values()):
                order[(drink, size)] += 1
        for drink in order.keys():
            response_string = response_string + str(order[drink]) + " " + drink[1] + " " + drink[0] + ', '
        return response_string

