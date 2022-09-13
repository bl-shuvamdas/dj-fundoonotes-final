from django.db import connection
from django.forms import model_to_dict
from note.models import Note
from rest_framework.response import Response
from rest_framework.views import APIView
from user.authentiation import verify_token


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetch_one(cursor):
    "Return rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))


# Create your views here.
class NoteRawQAPIView(APIView):
    @verify_token
    def get(self, request, pk=None):
        if pk is None:
            query_set = Note.objects.raw('SELECT * FROM note')
            data = list(map(lambda obj: model_to_dict(obj), query_set))
        else:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM note WHERE id = %s', [pk])
                data = dict_fetch_one(cursor)
        return Response({'data': data})

    @verify_token
    def post(self, request):
        title, description, user = request.data.values()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO note('title', 'description', 'user_id') VALUES (%s, %s, %s)",
                [title, description, user]
            )
            cursor.execute(
                "SELECT * FROM note WHERE title = %s AND description = %s AND user_id = %s ORDER BY id DESC LIMIT 1",
                [title, description, user])
            data = dict_fetch_one(cursor)
        return Response({'data': data}, status=201)

    @verify_token
    def put(self, request):
        pk, title, description, _ = request.data.values()
        with connection.cursor() as cursor:
            cursor.execute("UPDATE note SET title = %s, description = %s WHERE id = %s",
                           [title, description, pk])
            cursor.execute("SELECT * FROM note WHERE id = %s", [pk])
            data = dict_fetch_one(cursor)
        return Response({'data': data}, status=202)

    @verify_token
    def delete(self, request):
        pk, _ = request.data.values()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM note WHERE id = %s", [pk])
        return Response({'data': {}}, status=204)
