from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser ,Annonce, AnnonceImage




admin.site.register(CustomUser)
admin.site.register(Annonce)
admin.site.register(AnnonceImage)

