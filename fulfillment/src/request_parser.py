from google.auth import jwt
from config import Config

class RequestParser:

    def __init__(self, request):
        self.userid = ""
        self.username = ""
        self.conversation_token = ""
        self.original_detect_intent_request = {}
        self.parameters = {}
        self.intent = {}
        self.output_contexts = {}
        self.__parse__(request)

    def __decrypt_user_details(self, encrypted_text):
        # public_key = Config.certs_dict['db02ab30e0b75b8ecd4f816bb9e1978f62849894']
        # public_key = b'-----BEGIN CERTIFICATE-----\nMIIDJjCCAg6gAwIBAgIIJqxqI3wDgKkwDQYJKoZIhvcNAQEFBQAwNjE0MDIGA1UE\nAxMrZmVkZXJhdGVkLXNpZ25vbi5zeXN0ZW0uZ3NlcnZpY2VhY2NvdW50LmNvbTAe\nFw0xOTExMjAxNDQ5MzVaFw0xOTEyMDcwMzA0MzVaMDYxNDAyBgNVBAMTK2ZlZGVy\nYXRlZC1zaWdub24uc3lzdGVtLmdzZXJ2aWNlYWNjb3VudC5jb20wggEiMA0GCSqG\nSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCov+058bzmz1a7ZqjCIXe8+WxfxiRI5sGI\nzdf66e6dhSYmt/7Mn2bShJn0lc7FfDwK9JDuP6Kw9iifmfmh3qqhRh7lgus6zHuU\nxNC04U1LDU/jhtU3Gwm+41bQaaQhtYWmBCPmUgwpw0DmQAIIp0RiO+sWw614havs\nbLIz8gSfCmqNmGmXJTHj41npZD3T5BpYIWAZzPTKsrtmnkseNjBvRTLR7j6Q6jAM\nCM4ozH/6lA2sIN1ehBwfi/vT0hlfG80uy1EDNbngS1eBKW4Wvglrreyy3h0KatKc\nedcqMhp4f7734m0OpoojdzzHytBJHXzxrm/tNWCAxuYU57W2ikiFAgMBAAGjODA2\nMAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgeAMBYGA1UdJQEB/wQMMAoGCCsG\nAQUFBwMCMA0GCSqGSIb3DQEBBQUAA4IBAQA4gy3aHdPnEavhc91XB4bWvagPG5es\n/8aQtJdztDx0VGcWOe3BaBKRysujADJd/lRewKDLXNBeyOWwYEhp+5yOgV1W8Tzo\nF9JAS5i4oNMnuBfqxHHr7wXOLfK3ofTWbDDYMyhae8OeKQOW3zqj4No2J28jJ9J6\nZfChp80w2njkq4ySe+/KEX2sF4CLkjo/wtJADyKNs0bwq9HcVs6bklV/OMbfTJC9\nyLhI/X4Rpp4hRhqZk/lXZVBP2i79sY+ZgTvYzmfLwRdCJmx/AsNBrnMVlgBuGHcl\n5HUElpzuDphYkSWVM8Hkjf7qKLki/bW+NWLQYHvxKU8USyrHCOHLWtht\n-----END CERTIFICATE-----\n'
        user_details = jwt.decode(encrypted_text, verify=False)
        return user_details

    def __parse__(self, request):
        request_json = request.get_json(force=True)
        print(request_json)

        self.parameters = request_json.get('queryResult').get('parameters')
        self.intent = request_json.get('queryResult').get('intent')
        self.original_detect_intent_request = request_json.get('originalDetectIntentRequest')
        self.conversation_token = self.original_detect_intent_request['payload']['conversation']['conversationId']
        self.output_contexts = request_json.get('queryResult').get('outputContexts')

        payload = request_json.get('originalDetectIntentRequest').get('payload')
        if len(payload) == 0:
            # Testing from Dialogflow client
            self.userid = u'myUserId'
            self.username = u'myUserId'
        else:
            # Testing from Google Assistant
            user_details = payload.get('user')
            print(user_details)
            if "idToken" in user_details:
                # Authenticated user
                encrypted_user_info = user_details['idToken']
                decrypted_user_info = self.__decrypt_user_details(encrypted_user_info)
                # TODO Check if it is coming from your application
                self.username = decrypted_user_info['given_name']
                self.userid = decrypted_user_info['sub']
            else:
                # Guest user - Guest + converation Id
                self.userid = 'guest_'+ self.conversation_token
                self.username = 'guest user'