# cars/forms.py
from django import forms
from .models import Annonce, AnnonceImage

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'localisation', 'dedouaner', 
                  'marque', 'modele', 'annee', 'kilometrage', 
                  'carburant', 'transmission', 'prix', 'vignette']

