from certificates import Certificates


class Config:
    
    GOOGLE_PROJECT_ID = "order-buddy-257400"
    SESSION_ID = "order-buddy-257400-session"

    CURRENT_ORDER_COLLECTION = u'current_order'
    HISTORY_COLLECTION = u'current_item_count'

    certs_dict = Certificates.get()

    order_intent_drink_check_fulfillment_text = 'Drink name is not present'
    order_intent_size_check_fulfillment_text = 'Drink size is not present'
