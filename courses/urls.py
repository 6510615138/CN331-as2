from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_page/', views.user_page, name='user_page'),
    path('course_page/', views.course_page, name='course_page'),
    path('board_page/', views.board_page, name='board_page'),
    path('request_quota/', views.request_quota, name='request_quota'),
    path('cancel_quota/', views.cancel_quota, name='cancel_quota'),
    path('management/', views.management, name='management'),
]