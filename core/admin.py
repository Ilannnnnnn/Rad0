from django.contrib import admin
from .models import Profil, Evenement, Participation, Signalement


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'commune']
    search_fields = ['user__username', 'commune']


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date', 'lieu', 'organisateur', 'difficulte', 'nb_inscrits', 'max_participants']
    list_filter = ['difficulte', 'famille', 'date']
    search_fields = ['titre', 'lieu', 'description']
    date_hierarchy = 'date'


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['user', 'evenement', 'date_inscription', 'present', 'kg_collectes']
    list_filter = ['present', 'date_inscription']
    search_fields = ['user__username', 'evenement__titre']


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_dechet', 'traite', 'created_at']
    list_filter = ['type_dechet', 'traite', 'created_at']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
