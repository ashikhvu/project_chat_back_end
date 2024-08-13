from django.urls import path,re_path
from . import views 
from django.views.static import serve
from django.conf import settings

urlpatterns=[
    path('',views.Home.as_view(),name='home'),
    path('signup',views.SignUp.as_view(),name='signup'),
    path('signin',views.SignIn.as_view(),name='signin'),
    # for getting single user data with using id
    # also getting single user data of the currently loggedin user
    path('get_user_data',views.GetUserData.as_view(),name='get_user_data'),
    path('get_all_user_data',views.GetAllUserData.as_view(),name='get_all_user_data'),
    path('search_user',views.GetAllUserData.as_view(),name='search_user'),
    path('send_request',views.SendRequest.as_view(),name='send_request'),
    path('request_contact',views.RequestContact.as_view(),name='request_contact'),
    path('accept_request',views.SendRequest.as_view(),name='accept_request'),
    path('send_msg',views.ChatMessages.as_view(),name='send_msg'),
]