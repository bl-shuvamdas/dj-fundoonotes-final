from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentiation import verify_token
from .models import Note
from .serializers import NoteSerializer


# Create your views here.
class NoteAPIView(APIView):
    permission_classes = (AllowAny,)

    @verify_token
    def get(self, request):
        response = {'message': 'success', 'status': 200, 'data': {}}
        try:
            queryset = Note.objects.filter(user=request.query_params['user'])  # noqa
            serializer = NoteSerializer(queryset, many=True)
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])

    @verify_token
    def post(self, request):  # noqa
        response = {'message': 'Created', 'status': 201, 'data': {}}
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        return Response(response, status=response['status'])

    @verify_token
    def put(self, request):  # noqa
        response = {'message': 'accepted', 'status': status.HTTP_202_ACCEPTED, 'data': {}}
        try:
            queryset = Note.objects.get(pk=request.data['id'])  # noqa
            serializer = NoteSerializer(queryset, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])

    @verify_token
    def delete(self, request):  # noqa
        response = {'status': status.HTTP_204_NO_CONTENT, 'message': "no content"}
        try:
            queryset = Note.objects.get(pk=request.data['id'])  # noqa
            queryset.delete()
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])
