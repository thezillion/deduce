from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test),
    path('create_account', views.create_account),
    path('ask/', views.ask),
    path('answer/', views.answer),
]
