from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('test/', views.test),
    path('create_account/', views.create_account),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('password_reset/', views.password_reset, name='auth_password_reset'),
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    path('ask/', views.ask),
    path('answer/', views.answer),


]
