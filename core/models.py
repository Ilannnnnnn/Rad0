from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commune = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

    def total_participations(self):
        return self.user.participation_set.filter(present=True).count()

    def total_kg(self):
        return self.user.participation_set.aggregate(models.Sum('kg_collectes'))['kg_collectes__sum'] or 0


class Evenement(models.Model):
    DIFFICULTE_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    organisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    max_participants = models.IntegerField(default=20)
    difficulte = models.CharField(max_length=20, choices=DIFFICULTE_CHOICES, default='facile')
    famille = models.BooleanField(default=False, verbose_name="Adapté aux familles")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titre

    def nb_inscrits(self):
        return self.participation_set.count()

    def places_restantes(self):
        return self.max_participants - self.nb_inscrits()

    def est_complet(self):
        return self.nb_inscrits() >= self.max_participants


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)
    kg_collectes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'evenement']

    def __str__(self):
        return f"{self.user.username} - {self.evenement.titre}"


class Signalement(models.Model):
    TYPE_CHOICES = [
        ('plastique', 'Plastique'),
        ('verre', 'Verre'),
        ('metal', 'Métal'),
        ('mixte', 'Mixte'),
        ('autre', 'Autre'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    type_dechet = models.CharField(max_length=20, choices=TYPE_CHOICES)
    photo = models.ImageField(upload_to='signalements/', blank=True, null=True)
    traite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signalement {self.type_dechet} par {self.user.username}"
