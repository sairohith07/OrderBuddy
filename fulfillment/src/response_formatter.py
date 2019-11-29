from collections import Counter


class ResponseFormatter:

    def __init__(self, response_dict):
        self.response_dict = response_dict

    def format_cancel_intent_response(self):
        response_string = "Are you sure you want to cancel? Please say "
        for item_name in self.response_dict.keys():
            drink_name_dict = self.response_dict[item_name]
            for item_number in drink_name_dict.keys():
                customize_text = ','.join(drink_name_dict[item_number]['customize'])
                response_string += "," + item_number + " for " +drink_name_dict[item_number]['size'] + " " + item_name \
                                   + " " + ("" if customize_text.lower()=="no" else "With "+customize_text+" ")
        return response_string

    def format_delete_last_item_response(self,last_item_num,item_desc):
        response_string = "Are you sure you want to delete "+item_desc +" Please say "
        response_string+= str(last_item_num)+" to remove "+item_desc
        response_string+= " from your order or  say No! to abort"

        return response_string

    def format_complete_order(self):
        response_string = ""
        order = Counter()
        for drink in self.response_dict:
            for drink_params in self.response_dict[drink].values():
                order[(drink, drink_params["size"],','.join(drink_params["customize"]))] += 1
        for drink in order.keys():
            response_string = response_string + str(order[drink]) + " " \
                              + drink[1] + " " + drink[0] + ("" if drink[2].lower()=="no" else " With "+drink[2]) + ', '
        return response_string

    def format_cancel_item_not_exist(self):
        response_string = "This item is not part of the order. The items in the order are: "
        order_drinks = set()
        for drink in self.response_dict:
            order_drinks.add(drink)
        for drink_name in order_drinks:
            response_string = response_string + drink_name + ', '
        response_string = response_string + "Please say cancel along with the item to be removed"
        return response_string

    def format_empty_cart_response(self):
        response_string  = "Your cart is empty. Please add some items"
        return  response_string


