# Rad0 - Zero Déchets en Rade

Application web Django pour coordonner des ramassages de déchets sur la rade de Brest.

## Fonctionnalités

- Carte interactive des événements de nettoyage et signalements de pollution
- Création et gestion d'événements de ramassage
- Inscription aux événements
- Signalement de pollution avec géolocalisation
- Profil utilisateur avec statistiques
- Interface d'administration complète

## Technologies

- Django 5
- Bootstrap 5 (CDN)
- Leaflet.js pour la cartographie
- SQLite (base de données par défaut)

## Installation

1. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Appliquer les migrations :
```bash
python manage.py migrate
```

4. Charger les données de test (optionnel) :
```bash
python manage.py load_test_data
```

5. Créer un superutilisateur (si vous n'avez pas chargé les données de test) :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement :
```bash
python manage.py runserver
```

7. Ouvrir votre navigateur à l'adresse : http://localhost:8000

## Données de test

Si vous avez chargé les données de test, vous pouvez vous connecter avec :
- Username: `admin`
- Password: `admin`

Les données de test incluent :
- 3 événements de ramassage à venir autour de Brest
- 2 signalements de pollution
- Plusieurs utilisateurs de démonstration

## Interface d'administration

Accédez à l'interface d'administration Django : http://localhost:8000/admin

## Structure du projet

```
rad0/
├── rad0/                 # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Application principale
│   ├── models.py        # Modèles de données
│   ├── views.py         # Vues
│   ├── urls.py          # Routes
│   ├── forms.py         # Formulaires
│   └── admin.py         # Configuration admin
├── templates/           # Templates HTML
├── static/              # Fichiers statiques (CSS)
├── manage.py
└── requirements.txt
```

## Modèles

- **Profil** : Informations utilisateur étendues
- **Evenement** : Événements de ramassage de déchets
- **Participation** : Inscriptions aux événements
- **Signalement** : Signalements de pollution

## License

Projet éducatif - Libre d'utilisation