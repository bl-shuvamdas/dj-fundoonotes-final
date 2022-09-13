import requests as rq
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import CreateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from utils import JWT
from utils.email_service import Email

from .forms import SignInForm, SignUpForm
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
            Email.verify_user(email=serializer.data['email'])
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


class SignUpFormView(CreateView):
    form_class = SignUpForm
    model = User
    template_name = 'user/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['heading'] = 'Registrations'
        print(kwargs)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        url = '%s%s' % (settings.BASE_URL, reverse('auth:register'))
        if form.is_valid():
            response = rq.post(url, data=form.cleaned_data)

            if response.status_code == 201:
                messages.success(request, "Rgistration successfull")
                return redirect('home')

            messages.error(request, response.json()['message'])
            return render(request, self.template_name, {})
        return render(request, self.template_name, {})


class SignInFormView(CreateView):
    model = User
    template_name = 'user/signup.html'
    form_class = SignInForm

    def get_context_data(self, **kwargs):
        kwargs['heading'] = 'Login'
        print(kwargs)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        url = '%s%s' % (settings.BASE_URL, reverse('auth:login'))
        response = rq.post(url, data=request.POST)
        if response.status_code != 200:
            messages.error(request, response.json()['message'])
            return render(request, self.template_name, {})
        messages.success(request, "Login successfull")
        return redirect('home')
