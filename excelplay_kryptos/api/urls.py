from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('auth/', include('social_django.urls')),
    path('profile/', views.profile),
    path('leaderboard/', views.leaderboard),
    path('rank/', views.user_rank),
    path('test/', views.test),
    path('ask/', views.ask),
    path('answer/', views.answer),
    re_path(r'social/(?P<backend>[^/]+)/$', views.exchange_token),
    path('logout/', views.user_logout),
]
