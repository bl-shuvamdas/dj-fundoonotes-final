from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer


# Create your views here.
class NoteAPIView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get_queryset(request):
        return Note.objects.all()

    def get(self, request):
        response = {'message': 'success', 'status': 200, 'data': {}}
        try:
            queryset = self.get_queryset(request).filter(user=request.data['user'])
            serializer = NoteSerializer(queryset, many=True)
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])

    def post(self, request):
        response = {'message': 'Created', 'status': 201, 'data': {}}
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])

    def put(self, request):
        response = {'message': 'accepted', 'status': status.HTTP_202_ACCEPTED, 'data': {}}
        try:
            queryset = self.get_queryset(request).get(pk=request.data['id'])
            serializer = NoteSerializer(queryset, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response.update({"data": serializer.data})
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])

    def delete(self, request):
        response = {'status': status.HTTP_204_NO_CONTENT, 'message': "no content"}
        try:
            queryset = self.get_queryset(request).get(pk=request.data['id'])
            queryset.delete()
        except ValidationError as e:
            response.update({"message": e.detail, 'status': e.status_code})
        except Exception as e:
            response.update({"message": str(e), 'status': 400})
        return Response(response, status=response['status'])
