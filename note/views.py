from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentiation import verify_token
from .models import Note
from .serializers import NoteSerializer, CollaboratorSerializer


# Create your views here.
class NoteAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={200: NoteSerializer(many=True)})
    @verify_token
    def get(self, request):
        response = {'message': 'success', 'status': 200, 'data': {}}
        try:
            lookups = Q(user=request.data['user']) | Q(collaborator__id=request.data['user'])
            queryset = Note.objects.filter(lookups)  # noqa
            serializer = NoteSerializer(queryset, many=True)
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])

    @swagger_auto_schema(request_body=NoteSerializer)
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

    @swagger_auto_schema(request_body=NoteSerializer)
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id': openapi.Schema(title='ID', read_only=False, type=openapi.TYPE_INTEGER)}
        )
    )
    @verify_token
    def delete(self, request):  # noqa
        response = {'status': status.HTTP_204_NO_CONTENT, 'message': "no content"}
        try:
            queryset = Note.objects.get(pk=request.data['id'])  # noqa
            queryset.delete()
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])


class CollaboratorAPIView(APIView):
    @swagger_auto_schema(request_body=CollaboratorSerializer)
    @verify_token
    def put(self, request):  # noqa
        response = {'message': 'accepted', 'status': status.HTTP_202_ACCEPTED, 'data': {}}
        try:
            note = Note.objects.get(pk=request.data['id'], user=request.data['user'])  # noqa
            serializer = CollaboratorSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.update(data=serializer.data)
        except ValidationError as e:
            response.update(message=e.detail, status=e.status_code)
        except Exception as e:
            response.update(message=str(e), status=400)
        return Response(response, status=response['status'])

    @verify_token
    def delete(self, request):  # noqa
        response = {'status': status.HTTP_204_NO_CONTENT, 'message': "no content"}
        try:
            queryset = Note.objects.get(pk=request.data['id'], user=request.data['user'])  # noqa
            queryset.collaborator.clear()
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])
