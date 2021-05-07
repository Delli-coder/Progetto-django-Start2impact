from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', views.registration),
    path('homepage', views.home_page, name='homepage'),
    path('utente/<str:pk>', views.id_user),
    path('number_posts/', views.number_post),
    path('post_hours', views.hour_post),
    path('word', views.get_word)
]
