# Médiathèque Django

Projet Django réalisé dans le cadre de ma formation de développeur d'application web et mobile.

L'application permet de gérer les membres, les médias et les emprunts d'une médiathèque.

## Fonctionnalités principales

### Espace bibliothécaire

L'accès est protégé par l'authentification Django.

Il permet de :

- créer, modifier, supprimer et consulter les membres ;
- ajouter et consulter les médias ;
- créer et retourner des emprunts.

### Espace public

L'espace public permet de consulter les médias et leur disponibilité sans authentification.

### Règles d'emprunt

- Maximum de 3 emprunts simultanés par membre.
- Durée d'un emprunt : 7 jours.
- Un membre ayant un retard ne peut plus emprunter.
- Les livres, DVD et CD sont empruntables.
- Les jeux de plateau sont uniquement consultables.

## Installation

### 1. Créer l'environnement virtuel

Depuis le dossier du projet :

```cmd
python -m venv venv
```

Sous Windows :

```cmd
venv\Scripts\activate
```

### 2. Installer les dépendances

```cmd
pip install -r requirements.txt
```

### 3. Créer la base de données

```cmd
python manage.py migrate
```

### 4. Charger les données de démonstration

```cmd
python manage.py loaddata donnees_test
```

### 5. Créer un compte bibliothécaire

```cmd
python manage.py createsuperuser
```

Suivre les instructions afin de créer le nom d'utilisateur et le mot de passe.

### 6. Lancer le serveur

```cmd
python manage.py runserver
```

## Accès à l'application

Consultation publique :

```text
http://127.0.0.1:8000/medias/
```

Connexion bibliothécaire :

```text
http://127.0.0.1:8000/connexion/
```

Gestion des médias :

```text
http://127.0.0.1:8000/bibliothecaire/medias/
```

## Tests

Pour exécuter tous les tests automatisés :

```cmd
python manage.py test
```

Django utilise automatiquement une base de données de test isolée.

## Technologies

- Python
- Django 6.1.1
- SQLite
- HTML / Django Templates