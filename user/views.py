from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .serializers import ResisterSerializer, LoginSerializer


# Create your views here.
class RegisterApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = ResisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {"data": serializer.data, "status": 200}
        except ValidationError as e:
            response = {"message": e.detail, 'status': e.status_code}
        except Exception as e:
            response = {"message": str(e), 'status': 400}
        return Response(response, status=response['status'])


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

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
