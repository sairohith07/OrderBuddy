from test_cases_data import TestCasesData
from service import Service
from request_parser import RequestParser
import pytest
import json

# @pytest.fixture
# def get_sum_test_data():
#         return [(3,5,8), (-2,-2,-4), (-1,5,4), (3,-5,-2), (0,5,5)]
#
# def test_sum(get_sum_test_data):
#     for data in get_sum_test_data:
#         num1 = data[0]
#         num2 = data[1]
#         expected = data[2]
#         assert (num1+num2) == expected

@pytest.fixture
def get_test_order_intent_null():
    return [
        (TestCasesData.test_order_intent_null_1)
    ]

def test_order_intent_null(get_test_order_intent_null):
    for test_data in get_test_order_intent_null:
        request = RequestParser(test_data)
        response = Service.order_intent(request)
        assert response['fulfillmentText'] == 'Drink name is not present'