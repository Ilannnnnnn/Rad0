from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from core.models import Evenement, Signalement, Profil


class Command(BaseCommand):
    help = 'Charge des données de test pour Rad0'

    def handle(self, *args, **options):
        self.stdout.write('Création des données de test...')

        # Créer un utilisateur admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@rad0.fr',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin')
            admin.save()
            Profil.objects.create(user=admin, commune='Brest')
            self.stdout.write(self.style.SUCCESS('✓ Utilisateur admin créé (admin/admin)'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Utilisateur admin existe déjà'))

        # Créer quelques utilisateurs supplémentaires
        users = []
        for i, username in enumerate(['marie', 'pierre', 'julie'], 1):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                Profil.objects.create(user=user, commune=['Brest', 'Plougastel', 'Guipavas'][i-1])
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'✓ Utilisateur {username} créé'))

        # Créer 3 événements à venir
        evenements_data = [
            {
                'titre': 'Nettoyage de la plage du Moulin Blanc',
                'description': 'Ramassage de déchets sur la plage du Moulin Blanc. Matériel fourni : sacs, gants, pinces. Venez nombreux !',
                'date': timezone.now() + timedelta(days=7),
                'lieu': 'Plage du Moulin Blanc, Brest',
                'latitude': Decimal('48.3980'),
                'longitude': Decimal('-4.4350'),
                'difficulte': 'facile',
                'famille': True,
                'max_participants': 25,
            },
            {
                'titre': 'Opération rade propre - Port de commerce',
                'description': 'Collecte de déchets flottants et nettoyage des quais du port de commerce. Une action essentielle pour préserver notre rade.',
                'date': timezone.now() + timedelta(days=14),
                'lieu': 'Port de Commerce, Brest',
                'latitude': Decimal('48.3830'),
                'longitude': Decimal('-4.4950'),
                'difficulte': 'moyen',
                'famille': False,
                'max_participants': 15,
            },
            {
                'titre': 'Sortie kayak - Ramassage macro-déchets',
                'description': 'Sortie en kayak pour ramasser les déchets dans les zones difficiles d\'accès. Expérience en kayak requise. Kayaks fournis.',
                'date': timezone.now() + timedelta(days=21),
                'lieu': 'Base nautique de Plougastel',
                'latitude': Decimal('48.3750'),
                'longitude': Decimal('-4.3680'),
                'difficulte': 'difficile',
                'famille': False,
                'max_participants': 10,
            },
        ]

        for data in evenements_data:
            evenement, created = Evenement.objects.get_or_create(
                titre=data['titre'],
                defaults={**data, 'organisateur': admin}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Événement créé: {data["titre"]}'))

        # Créer 2 signalements
        signalements_data = [
            {
                'latitude': Decimal('48.3900'),
                'longitude': Decimal('-4.4800'),
                'description': 'Pneus abandonnés sur le rivage',
                'type_dechet': 'mixte',
                'traite': False,
            },
            {
                'latitude': Decimal('48.3820'),
                'longitude': Decimal('-4.4600'),
                'description': 'Nombreuses bouteilles en plastique et canettes',
                'type_dechet': 'plastique',
                'traite': False,
            },
        ]

        for data in signalements_data:
            signalement, created = Signalement.objects.get_or_create(
                latitude=data['latitude'],
                longitude=data['longitude'],
                defaults={**data, 'user': admin}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Signalement créé: {data["description"]}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Données de test chargées avec succès !'))
        self.stdout.write('\n📝 Vous pouvez vous connecter avec :')
        self.stdout.write('   - Username: admin')
        self.stdout.write('   - Password: admin')
