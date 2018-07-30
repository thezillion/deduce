from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test),
    path('create_account', views.create_account),
    path('login', views.login_user),
    path('logout', views.logout_user),
    path('change_password', views.ChangePasswordView.as_view()),
    path('ask/', views.ask),
    path('answer/', views.answer),

]
