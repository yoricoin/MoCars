from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import datetime

class CustomUser(AbstractUser):
   
    

    USER_TYPES = (
        ('particulier', 'Particulier'),
        ('professionnel', 'Professionnel'),
    )
    ROLE_TYPES = (
        ('user', 'Utilisateur'),
        ('moderateur', 'Modérateur'),
        ('admin', 'Administrateur'),
    )
    

    user_type = models.CharField(max_length=13, choices=USER_TYPES, default='particulier', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_TYPES, default='user')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    terms = models.BooleanField(default=False)

    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        default="profile_pics/default.png",
        blank=True,
        null=True
    )

    
    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"







class Annonce(models.Model):
    # Statut de l'annonce
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
        ('vendu', 'Vendu'),
    )

    # Relation avec l'utilisateur (vendeur)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="annonces"
    )

    # Infos véhicule
    titre = models.CharField(max_length=200)
    dedouaner = models.BooleanField(default=False)
    description = models.TextField()
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.PositiveIntegerField()
    kilometrage = models.PositiveIntegerField()
    carburant = models.CharField(
        max_length=20,
        choices=(
            ('essence', 'Essence'),
            ('diesel', 'Diesel'),
            ('hybride', 'Hybride'),
            ('electrique', 'Électrique'),
        )
    )
    transmission = models.CharField(
        max_length=20,
        choices=(
            ('manuelle', 'Manuelle'),
            ('automatique', 'Automatique'),
        )
    )
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    localisation = models.CharField(max_length=200, blank=True)

    # Vignette = taxe annuelle
    vignette = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Statut de l'annonce
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titre} - {self.utilisateur.username}"


class AnnonceImage(models.Model):
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="annonces/photos/")

    def clean(self):
        # Limite de 10 images par annonce
        if self.annonce and self.annonce.images.count() >= 10:
            raise ValidationError("Une annonce ne peut pas avoir plus de 10 images.")

    def __str__(self):
        return f"Image de {self.annonce.titre}"
    



class PasswordResetCode(models.Model):
    """Stocke les codes de vérification pour la réinitialisation"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    verification_method = models.CharField(max_length=10, choices=[('email', 'Email'), ('sms', 'SMS')])
    
    class Meta:
        ordering = ['-created_at']
    
    def is_valid(self):
        """Le code est valide pendant 10 minutes"""
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() < expiry_time and not self.is_used
    
    def __str__(self):
        return f"{self.user.email} - {self.code} - {'Valide' if self.is_valid() else 'Expiré'}"