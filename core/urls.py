from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carte/', views.carte, name='carte'),
    path('evenement/<int:pk>/', views.evenement_detail, name='evenement_detail'),
    path('evenement/nouveau/', views.creer_evenement, name='creer_evenement'),
    path('evenement/<int:pk>/modifier/', views.modifier_evenement, name='modifier_evenement'),
    path('evenement/<int:pk>/supprimer/', views.supprimer_evenement, name='supprimer_evenement'),
    path('evenement/<int:pk>/inscription/', views.inscription_evenement, name='inscription_evenement'),
    path('evenement/<int:pk>/desinscription/', views.desinscription_evenement, name='desinscription_evenement'),
    path('signaler/', views.signaler, name='signaler'),
    path('profil/', views.profil, name='profil'),
    path('register/', views.register, name='register'),
]
