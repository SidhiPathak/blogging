from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .serializers import *
from .models import *
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.


# User Sign up
@csrf_exempt 
def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = UserSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        return JsonResponse(serializers.errors, status=400)
    
# Logging User In    
class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

# Forget Password Api
@csrf_exempt 
def request_reset_email(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = SendPasswordResetEmailSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            msg = "Password Reset link send. Please check your email."
            response = {'status': 'success','code': status.HTTP_200_OK,'message': msg}
            return JsonResponse(response, status=201)
        return JsonResponse(serializers.errors, status=400)

# Reset Password
@csrf_exempt
def resetPassword(request, uid, token):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = UserPasswordResetSerializer(data = data, context = {'uid':uid, 'token': token})
        if serializers.is_valid(raise_exception=True):
            msg = "Password Reset successfully"
            response = {'status': 'success','code': status.HTTP_200_OK,'message': msg}
            return JsonResponse(response, status=201)
        return JsonResponse(serializers.errors, status=400)

from django.template.response import TemplateResponse    
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogSerializer

    def list(self, request, *args, **kwargs):
        queryset = Blogs.objects.filter(status="publish").order_by('-created_at')
        serializer = BlogSerializer(queryset, many=True)
        result = serializer.data
        # Render the custom template with the articles data
        return TemplateResponse(request, 'blog_list.html', {'preview': result})

    def retrieve(self, request, *args, **kwargs):
        self.template_name = 'post_detail.html'
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return render(request, self.template_name, {'serializer': serializer.data})
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk):
        getData = request.data
        base_url = request.build_absolute_uri()
        eMailTemplate = f"""
        Hi {getData.get('receiver')},
        Here is my new blog post related to {getData.get('topic')}. Hope you like it.
        Blog Link:- base_url/{pk}/
        Thank you.
        with regards,
        {request.user.username}
        """
        email = getData.get('receiver_email')
        status = send_email(getData.get('topic'),eMailTemplate,email)
        return Response('Success')

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer