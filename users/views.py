import jwt

from json.decoder import JSONDecodeError

from django.views import View
from django.http import JsonResponse

from users.models import User
from users.kakao import KaKaoAPI
from ifLearn.settings import SECRET_KEY, ALGORITHM

class KaKaoLoginView(View):
    def post(self, request):
        try:
            kakao_access_token = request.headers['Authorization']
            kakao_user = KaKaoAPI(kakao_access_token)
            response = kakao_user.get_kakao_user()

            if not response.status_code == 200:
                return JsonResponse({'message' : 'INVALID TOKEN'}, status = 401)

            user_information = response.json()

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status = 400)

        user = User.objects.get_or_create(
            kakao_id   = user_information.get('id'),
        )

        encoded_jwt = jwt.encode({'id' : user[0].id}, SECRET_KEY, algorithm = ALGORITHM)
        return JsonResponse({'access_token' : encoded_jwt}, status = 200)