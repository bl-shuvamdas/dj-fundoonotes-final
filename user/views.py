from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from utils import JWT

from .models import User
from .serializers import LoginSerializer, ResisterSerializer


# Create your views here.
class RegisterApiView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ResisterSerializer)
    def post(self, request):
        try:
            serializer = ResisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"data": serializer.data, "status": 201}
        except ValidationError as e:
            response = {"message": e.detail, 'status': e.status_code}
        except Exception as e:
            response = {"message": str(e), 'status': 400}
        return Response(response, status=response['status'])


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"data": serializer.data, "status": 200}
        except ValidationError as e:
            response = {"message": e.detail, 'status': e.status_code}
        except Exception as e:
            response = {"message": str(e), 'status': 400}
        return Response(response, status=response['status'])


class VerifyUser(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        response = {'message': 'user verified', "status": 200}
        try:
            payload = JWT.decode(token)
            del payload['exp']
            user = User.objects.get(**payload)
            user.is_verify = True
            user.save()
        except Exception as e:
            response.update({'message': str(e), "status": 400})
        return Response(response, status=response['status'])
