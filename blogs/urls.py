from django.urls import path, include, re_path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'blogs', BlogViewSet)
router.register(r'comments', CommentsViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('signup/', signup, name='register-new-user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('request-reset-email/', request_reset_email, name = 'request-reset-email'),
    re_path(r"^reset-password/(?P<uid>[-\w]+)_(?P<token>[-\w]+)/$", resetPassword, name="reset-password")
]