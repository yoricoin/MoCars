🌎 [Version Française](#-mocars---plateforme-de-petites-annonces-de-véhicules) | [English Version](#-mocars---vehicle-classifieds-platform)

---

# 🚗 Mocars - Plateforme de Petites Annonces de Véhicules

Mocars est une application web moderne développée avec **Django** permettant la publication, la gestion et la recherche de petites annonces pour l'achat et la vente de véhicules. La plateforme est conçue pour les utilisateurs particuliers et professionnels, avec un workflow complet de modération et des outils de sécurité intégrés (SMS & E-mail).

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

### 2. Cloner le projet
```bash
git clone https://github.com/yoricoin/MoCars.git
cd MoCars/projet
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
    │   └── views.py             # Contrôleurs et logique métier
    │
    ├── templates/               # Modèles de pages HTML
    │   ├── base.html            # Structure HTML globale
    │   ├── pages/               # Pages de l'application (home, register, profile, chat...)
    │   ├── parts/               # Blocs réutilisables (header, footer)
    │   └── admindash/           # Interface d'administration
    │
    └── static/                  # Fichiers statiques (images, scripts JS, styles CSS)
```

---
---

# 🚗 Mocars - Vehicle Classifieds Platform

Mocars is a modern web application built with **Django** designed for listing, managing, and searching vehicles for sale. The platform is designed for both individual and professional users, featuring a complete moderation workflow and integrated security features (SMS & Email verification).

## ✨ Features

### 👤 Account & Profile Management
- **Account Types**: Individual (Particulier) or Professional (Professionnel).
- **User Roles**: Standard user (`user`), Moderator (`moderateur`), and Administrator (`admin`).
- **Detailed Profiles**: Manage personal details, phone numbers, cities, addresses, postal codes, and custom profile pictures.
- **Enhanced Security**: Secure password reset using temporary 6-digit verification codes (valid for 10 minutes) sent via **Email** (SMTP) or **SMS** (via Twilio).

### 📝 Vehicle Listings (Annonces)
- **Create & Edit**: Publish detailed car listings including title, description, brand, model, year, mileage, fuel type (gasoline, diesel, hybrid, electric), transmission type (manual, automatic), price, location, annual tax (vignette), and customs clearance status.
- **Image Uploads**: Upload up to 10 photos per listing with size (max 5MB) and format (JPEG, PNG, GIF, WebP) validations.
- **Listing Lifecycle**: Real-time status management (Pending, Approved, Rejected, Sold).

### 🛠️ Moderation & Admin Dashboard
- **Admin Dashboard**: Live statistics of the platform (total listings, approved, pending, rejected).
- **Listing Moderation**: Approve or reject pending listings individually or in bulk.
- **User Management**: Promote standard users to moderators, demote, or delete accounts.

### 🔍 Advanced Search & Filters
- Keyword search in listing titles.
- Filter by brand, max price, and min year.
- Sort listings by date (newest first), price (ascending/descending), or mileage.

---

## 🛠️ Tech Stack
- **Backend**: Django 5.1.7 (Python 3)
- **Database**: SQLite 3 (default, customizable)
- **Image Processing**: Pillow
- **External APIs**: 
  - **Twilio API** for SMS verification codes.
  - **SMTP / Gmail** for email verification codes.

---

## 🚀 Installation and Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** and **pip** installed.

### 2. Clone the Project
```bash
git clone https://github.com/yoricoin/MoCars.git
cd MoCars/projet
```

### 3. Create and Activate a Virtual Environment
On Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
Install the required packages to run the application:
```bash
pip install django python-decouple twilio pillow requests
```

### 5. Environment Variables (`.env`)
Create a `.env` file in the `projet/projet/` directory (next to `settings.py`) and set the following keys:
```ini
# Email Settings (SMTP)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Twilio Settings (SMS)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### 6. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an Admin Account (Superuser)
```bash
python manage.py createsuperuser
```

### 8. Start the Development Server
```bash
python manage.py runserver
```
Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📁 Project Structure

```text
Mocars/
│
└── projet/
    ├── manage.py                # Django entry point
    ├── db.sqlite3               # Local SQLite development database
    │
    ├── projet/                  # Project configuration folder
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py          # App settings
    │   ├── urls.py              # URL routing
    │   └── wsgi.py
    │
    ├── cars/                    # Main app directory
    │   ├── admin.py             # Django admin configuration
    │   ├── forms.py             # Form classes
    │   ├── middleware.py        # Custom middlewares
    │   ├── models.py            # App database models
    │   ├── urls.py              # App routing
    │   └── views.py             # Controllers and business logic
    │
    ├── templates/               # HTML Templates
    │   ├── base.html            # Core layout
    │   ├── pages/               # Functional pages
    │   ├── parts/               # Reusable blocks (header, footer)
    │   └── admindash/           # Administration dashboard templates
    │
    └── static/                  # Static assets (images, JS scripts, CSS styles)
```
