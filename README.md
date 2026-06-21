# 🚗 Mocars - Plateforme de Petites Annonces de Véhicules

Mocars est une application web moderne développée avec **Django** permettant la publication, la gestion et la recherche de petites annonces pour l'achat et la vente de véhicules. La plateforme est conçue pour les utilisateurs particuliers et professionnels, avec un workflow complet de modération et des outils de sécurité intégrés (SMS & E-mail).

---

## ✨ Fonctionnalités

### 👤 Gestion des Comptes & Profils
- **Types de Comptes** : Particulier ou Professionnel.
- **Rôles Utilisateurs** : Simple utilisateur (`user`), Modérateur (`moderateur`) et Administrateur (`admin`).
- **Profil Détaillé** : Informations personnelles, numéro de téléphone, ville, adresse, code postal et photo de profil personnalisable.
- **Sécurité renforcée** : Réinitialisation de mot de passe via un code à 6 chiffres temporaire (valide 10 minutes) envoyé par **E-mail** (SMTP) ou par **SMS** (via Twilio).

### 📝 Annonces de Véhicules
- **Ajout & Modification** : Publication d'annonces détaillées avec titre, description, marque, modèle, année, kilométrage, type de carburant, type de transmission, prix, localisation, montant de la taxe annuelle (vignette) et statut de dédouanement.
- **Gestion d'images** : Support pour télécharger jusqu'à 10 photos par annonce avec validation de taille (max 5 Mo) et de format (JPEG, PNG, GIF, WebP).
- **Cycle de vie** : Statut d'annonce modifiable (En attente, Approuvé, Rejeté, Vendu).

### 🛠️ Espace Administration & Modération
- **Dashboard Admin** : Vue d'ensemble des statistiques de la plateforme (nombre total d'annonces, annonces approuvées, rejetées ou en attente).
- **Modération des Annonces** : Approbation ou rejet individuel ou en masse (actions groupées).
- **Gestion des Utilisateurs** : Promotion en modérateur, rétrogradation ou suppression de compte.

### 🔍 Recherche & Filtres Avancés
- Recherche par mot-clé dans les titres.
- Filtrage par marque, prix maximum et année minimale.
- Tri des résultats par date (les plus récentes), par prix (croissant/décroissant) ou par kilométrage.

---

## 🛠️ Stack Technique
- **Backend** : Django 5.1.7 (Python 3)
- **Base de données** : SQLite 3 (par défaut, personnalisable)
- **Traitement d'images** : Pillow
- **APIs Externes** : 
  - **Twilio API** pour l'envoi de codes par SMS.
  - **SMTP / Gmail** pour l'envoi de courriels.

---

## 🚀 Installation et Démarrage

### 1. Prérequis
Assurez-vous d'avoir installé **Python 3.10+** et **pip** sur votre machine.

### 2. Cloner le projet (si ce n'est pas déjà fait)
```bash
git clone https://github.com/yoricoin/Mocars.git
cd Mocars/projet
```

### 3. Créer et activer un environnement virtuel
Sur Windows :
```powershell
python -m venv .venv
.venv\Scripts\activate
```
Sur macOS/Linux :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Installer les dépendances
Installez les packages nécessaires au fonctionnement de l'application :
```bash
pip install django python-decouple twilio pillow requests
```

### 5. Configuration des variables d'environnement (`.env`)
Créez un fichier `.env` dans le dossier `projet/projet/` (au même niveau que `settings.py`) et configurez les clés suivantes :
```ini
# Configuration des e-mails (SMTP)
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-d-application

# Configuration Twilio (SMS)
TWILIO_ACCOUNT_SID=votre_account_sid
TWILIO_AUTH_TOKEN=votre_auth_token
TWILIO_PHONE_NUMBER=votre_numero_twilio
```

### 6. Appliquer les migrations de la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Créer un compte administrateur (Superuser)
```bash
python manage.py createsuperuser
```

### 8. Lancer le serveur de développement
```bash
python manage.py runserver
```
L'application sera accessible à l'adresse : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📁 Structure du Projet

```text
Mocars/
│
└── projet/
    ├── manage.py                # Point d'entrée de l'application Django
    ├── db.sqlite3               # Base de données SQLite de développement
    │
    ├── projet/                  # Configuration principale du projet Django
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py          # Paramètres de l'application (base de données, e-mail, etc.)
    │   ├── urls.py              # Configuration générale des URL
    │   └── wsgi.py
    │
    ├── cars/                    # Application principale de gestion des voitures
    │   ├── admin.py             # Enregistrement des modèles dans l'interface admin
    │   ├── forms.py             # Formulaires Django (AnnonceForm)
    │   ├── middleware.py        # Middlewares (RefreshUserMiddleware)
    │   ├── models.py            # Modèles de données (CustomUser, Annonce, AnnonceImage...)
    │   ├── urls.py              # Routes associées aux vues de l'application cars
    │   └── views.py             # Contrôleurs et logique métier (1000+ lignes)
    │
    ├── templates/               # Modèles de pages HTML
    │   ├── base.html            # Structure HTML globale
    │   ├── pages/               # Pages de l'application (home, register, profile, chat...)
    │   ├── parts/               # Blocs réutilisables (header, footer)
    │   └── admindash/           # Interface d'administration
    │
    └── static/                  # Fichiers statiques (images, scripts JS, styles CSS)
```
