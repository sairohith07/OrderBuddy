from collections import Counter


class ResponseFormatter:

    def __init__(self, response_dict):
        self.response_dict = response_dict

    def format_cancel_intent_response(self):
        response_string = "Please say "
        for item_name in self.response_dict.keys():
            drink_name_dict = self.response_dict[item_name]
            for item_number in drink_name_dict.keys():
                response_string += "," + item_number + " for " +drink_name_dict[item_number]['size'] +" "+ item_name + " "
        return response_string

    def format_delete_last_item_response(self,last_item_num,item_desc):
        response_string = "Are you sure you want to delete the last item? Please say "
        response_string+= str(last_item_num)+" to remove "+item_desc
        response_string+= " from your order or No! to abort cancel"

    def format_complete_order(self):
        response_string = "This item is not part of the order. The items in the order are: "
        order_drinks = set()
        for drink in list(self.response_dict.keys()):
            order_drinks.add(drink)
        for drink_name in order_drinks.keys():
            response_string = response_string + drink_name + ', '
        response_string = response_string + "Please say Cancel along with the item to be removed"
        return response_string
    def format_cancel_item_intent_no(self):
        response_sring = "Lets continue with your order.  Do you want to add anything else?"

