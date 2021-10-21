from django.test   import TestCase, Client
from unittest.mock import MagicMock, patch

class UserTest(TestCase):
    @patch('users.kakao.requests')
    def test_kakao_login_response_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 200 
            
            def json(self):
                return {
                    'id'           : 1957405410,
                    'connected_at' : '2021-10-20T09:40:27Z', 
                    'properties'   : {'nickname': '김동휘'}, 
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False, 
                        'profile'                         : {'nickname': '김동휘'}, 
                        'has_email'                       : True, 
                        'email_needs_agreement'           : False, 
                        'is_email_valid'                  : True, 
                        'is_email_verified'               : True, 
                        'email'                           : 'dwhxx@kakao.com', 
                        'has_gender'                      : True, 
                        'gender_needs_agreement'          : False, 
                        'gender'                          : 'male'
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "lqV8TBkiKBJhzwnAsqeD96FcZDjFC7xZf6oMEwopcJ8AAAF8oO7ZIQ"} 
        response            = client.post("/users/login", **headers) 

        self.assertEqual(response.status_code, 200)
    
    @patch('users.kakao.requests')
    def test_kakao_login_user_fail(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 401
            def json(self):
                return {'msg': 'this access token does not exist', 'code': -401}
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "lqV8TBkiKBJhzwnAsqeD96FcZDjFC7xZf6oMEwopcJ8AAAF8oO7ZIQ"} 
        response            = client.post("/users/login", **headers) 

        self.assertEqual(response.status_code, 401)
    

