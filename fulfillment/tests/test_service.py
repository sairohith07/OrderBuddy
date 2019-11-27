from test_cases_data import TestCasesData
from app import app
import pytest
import json
from config import Config

class TestService:

    @pytest.fixture
    def get_test_order_intent_drink_check(self):
        return [
            (TestCasesData.test_order_intent_drink_null),
            (TestCasesData.test_order_intent_drink_empty)
        ]

    def test_order_intent_drink_check(self, get_test_order_intent_drink_check):
        for test_data in get_test_order_intent_drink_check:
            response = app.test_client().post(
                '/webhook',
                data=json.dumps(test_data),
                content_type='application/json',
            )

            data = json.loads(response.get_data(as_text=True))
            print(data)
            print(data['fulfillmentText'])

            assert data['fulfillmentText'] == Config.order_intent_drink_check_fulfillment_text

    @pytest.fixture
    def get_test_order_intent_size_check(self):
        return [
            (TestCasesData.test_order_intent_size_null),
            (TestCasesData.test_order_intent_size_empty)
        ]

    def test_order_intent_size_check(self, get_test_order_intent_size_check):
        for test_data in get_test_order_intent_size_check:
            response = app.test_client().post(
                '/webhook',
                data=json.dumps(test_data),
                content_type='application/json',
            )

            data = json.loads(response.get_data(as_text=True))
            print(data)
            print(data['fulfillmentText'])

            assert data['fulfillmentText'] == Config.order_intent_size_check_fulfillment_text

    @pytest.fixtures
    def clear_document(self):
        return[
            (TestCasesData.clear_document_cancel_order)
            (TestCasesData.clear_document_cancel_order_yes_followup)
        ]

    @pytest.fixture
    def get_complete_order_intent__null_check(self):
        return [
            (TestCasesData.test_complete_order_intent_null_document)
        ]

    # helper function to delete document by issuing cancel order
    def clear_document_helper(self):
        data_array = [
            (TestCasesData.clear_document_cancel_order)
            (TestCasesData.clear_document_cancel_order_yes_followup)
        ]
        for test_data in data_array:
            app.test_client().post(
                '/webhook',
                data=json.dumps(test_data),
                content_type='application/json',
            )

    def test_complete_order_intent__null_check(self,get_complete_order_intent__null_check):
        # nullifies the document by cancelling order
        self.clear_document_helper()
        for test_data in get_complete_order_intent__null_check:
            response = app.test_client().post(
                '/webhook',
                data=json.dumps(test_data),
                content_type='application/json',
            )
            data = json.loads(response.get_data(as_text=True))
            print(data)
            print(data['fulfillmentText'])
            assert data['fulfillmentText'] == Config.null_document_default_response_text

