# views.py
import json
import os
from time import timezone
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login , authenticate ,logout
from django.core.paginator import Paginator
from django.urls import reverse
from requests import Session
from django.contrib.auth import update_session_auth_hash
from cars.forms import AnnonceForm
from .models import CustomUser, Annonce, AnnonceImage, PasswordResetCode
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
import sys
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone  
from django.conf import settings
from twilio.rest import Client
from django.core.paginator import Paginator
from datetime import datetime as dt
import datetime







def home(request):
    return render(request, 'pages/home.html')

def mesannonces(request):
    annonces = Annonce.objects.filter(utilisateur=request.user)
    return render(request, 'pages/mesannonces.html', {"annonces": annonces})
def gererannonce(request):
    annonces = Annonce.objects.all()
    return render(request, 'admindash/gererannonce.html', {"annonces": annonces})




def contact(request):
    return render(request, 'pages/contact.html')


def about(request):
    return render(request, 'pages/about.html')

@login_required
def parametres(request):
    return render(request, 'pages/parametres.html')

@login_required
def code(request):
    return render(request, 'pages/codeverif.html')

@login_required
def oublie(request):
    return render(request, 'pages/oublie.html')



@login_required
def supprimermoncompte(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès. Cette action est irréversible.")
        return redirect("home")
    
    # Affiche une page de confirmation
    return render(request, "pages/confirmer_suppression.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            form = {
                'error': "Les mots de passe ne correspondent pas.",
                'username': username,
                'email': email
            }
            return render(request, 'pages/register.html', {'form': form})
    return render(request, 'pages/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        personne = CustomUser.objects.filter(email=email).first()
        if personne:
            user = authenticate(request, username=personne.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'pages/login.html', {'error': "Email ou mot de passe incorrect."})
    return render(request, 'pages/login.html')
  
@login_required 
def logout_view(request):
    logout(request)
    return redirect('home') 


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        # Upload photo AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'profile_picture' in request.FILES:
            if user.profile_picture and user.profile_picture.name != 'profile_pics/default.png':
                old_image_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            user.profile_picture = request.FILES['profile_picture']
            user.save()
            return JsonResponse({'success': True, 'profile_picture_url': user.profile_picture.url})

        # Mise à jour du profil (formulaires classiques)
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.postal_code = request.POST.get('postal_code', user.postal_code)
        user.user_type = request.POST.get('user_type', user.user_type)
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            user.date_of_birth = date_of_birth
        
        # If user.terms is a BooleanField, keep as is:
        user.terms = 'terms' in request.POST

        # If user.terms is a DateTimeField, use:
        # if 'terms' in request.POST:
        #     user.terms = datetime.datetime.now()

        # If user.terms is a CharField, use:
        # user.terms = request.POST.get('terms', user.terms)
        user.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('profile')

    return render(request, 'pages/profile.html', {'user': user})






@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Vérifications
        if not user.check_password(current_password):
            return JsonResponse({"success": False, "field": "current_password", "message": "Le mot de passe actuel est incorrect."})
        elif new_password != confirm_password:
            return JsonResponse({"success": False, "field": "confirm_password", "message": "Les mots de passe ne correspondent pas."})
        elif current_password == new_password:
            return JsonResponse({"success": False, "field": "new_password", "message": "Le nouveau mot de passe doit être différent de l'ancien."})
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"success": True})

    # Pour les GET classiques
    return render(request, 'pages/change_password.html')


@login_required
def ajouter_annonce(request):
    user = request.user
    champs_obligatoires = [
        user.first_name,
        user.last_name,
        user.email,
        user.phone,   # ton champ tel
        user.city,    # ta ville
        user.address  # ton adresse
    ]
    if any(not champ for champ in champs_obligatoires):
        messages.error(request, "⚠️ Veuillez compléter votre profil avant de publier une annonce.")
        return redirect('profile')  # redirige vers la page profil
    marques = ['BMW', 'Audi', 'Mercedes', 'Volkswagen', 'Renault', 'Peugeot']  # à adapter
    current_year = datetime.datetime.now().year
    annees = list(range(current_year, current_year - 30, -1))  # Dernières 30 années
    data = {}
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.utilisateur = request.user
            annonce.save()
            if len(files) > 10:
                messages.error(request, "Vous ne pouvez pas ajouter plus de 10 images.")
                annonce.delete()
            for f in files:
                AnnonceImage.objects.create(annonce=annonce, image=f)
            messages.success(request, "Votre annonce a été ajoutée avec succès !")
            return redirect('mesannonces')
            
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
            data = request.POST
    else:
        form = AnnonceForm()
    context = {
        'form': form,
        'data': data,
        'marques': marques,
        'annees': annees,
    }
    return render(request, 'pages/ajouterannonce.html', context)


@login_required
def detail_annonce(request, annonce_id):
    """
    Affiche les détails d'une annonce spécifique.
    """
    # On récupère l'annonce correspondant à l'ID, ou une erreur 404 si elle n'existe pas.
    # prefetch_related('images') est une optimisation pour charger toutes les images
    # en une seule requête SQL supplémentaire, c'est plus efficace.
    annonce = get_object_or_404(Annonce.objects.prefetch_related('images'), pk=annonce_id)
    
    # On passe l'objet 'annonce' au template dans un dictionnaire de contexte.
    context = {
        'annonce': annonce
    }
    
    # On retourne le template HTML avec les données de l'annonce.
    return render(request, 'pages/detail_annonce.html', context)




def chat(request):
    return render(request, 'pages/chat.html')


@login_required
def supprimer_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, pk=annonce_id, utilisateur=request.user)

    if request.method == 'POST':
        # Supprimer les images associées
        for image in annonce.images.all():
            if image.image and default_storage.exists(image.image.name):
                default_storage.delete(image.image.name)
            image.delete()
        
        # Supprimer l'annonce
        annonce.delete()

        # Vérifier si c’est un appel AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Annonce supprimée avec succès'})
        else:
            messages.success(request, "Annonce supprimée avec succès.")
            return redirect('mesannonces')  # adapte le nom de ta vue de liste

    # Mauvaise méthode
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect('mesannonces')









@login_required
def edit_annonce(request, annonce_id):
    """
    Vue pour modifier une annonce existante
    """
    # Récupérer l'annonce et vérifier que l'utilisateur en est propriétaire
    annonce = get_object_or_404(Annonce, id=annonce_id, utilisateur=request.user)
    
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=annonce)
        
        if form.is_valid():
            # Sauvegarder les modifications de l'annonce
            updated_annonce = form.save(commit=False)
            updated_annonce.utilisateur = request.user
            updated_annonce.save()
            
            # Traiter les nouvelles images uploadées depuis le champ file input
            uploaded_files = request.FILES.getlist('imageUpload')
            if uploaded_files:
                handle_image_uploads(request, updated_annonce, uploaded_files)
            
            messages.success(
                request, 
                'Votre annonce a été mise à jour avec succès!'
            )
            return redirect('detail_annonce', annonce_id=updated_annonce.id)
        else:
            # Ajouter les classes CSS aux champs avec erreurs
            for field_name, errors in form.errors.items():
                if field_name in form.fields:
                    form.fields[field_name].widget.attrs['class'] = 'form-control error'
                    
            messages.error(
                request, 
                'Veuillez corriger les erreurs dans le formulaire.'
            )
    else:
        form = AnnonceForm(instance=annonce)
    
    # Ajouter les classes CSS aux champs du formulaire
    for field_name, field in form.fields.items():
        css_classes = 'form-control'
        if field_name in ['titre', 'description', 'marque', 'modele', 'annee', 
                         'kilometrage', 'carburant', 'transmission', 'prix']:
            field.widget.attrs['required'] = True
            
        if field_name == 'description':
            field.widget.attrs['rows'] = 5
            field.widget.attrs['placeholder'] = 'Décrivez votre véhicule en détail...'
            
        if field_name in ['prix', 'vignette']:
            field.widget.attrs['placeholder'] = 'Montant en MAD'
            field.widget.attrs['step'] = '0.01'
            
        if field_name == 'kilometrage':
            field.widget.attrs['placeholder'] = 'Kilométrage en km'
            
        if field_name == 'annee':
            field.widget.attrs['min'] = 1950
            field.widget.attrs['max'] = 2025
            
        if field_name == 'localisation':
            field.widget.attrs['placeholder'] = 'Ville, région...'
            
        field.widget.attrs['class'] = css_classes
    
    context = {
        'form': form,
        'annonce': annonce,
        'page_title': f'Modifier - {annonce.titre}',
        'current_images': annonce.images.all(),
        'max_images': 10,
        'current_image_count': annonce.images.count(),
    }
    
    return render(request, 'pages/edit_annonce.html', context)

@login_required
@require_POST
def delete_annonce_image(request, image_id):
    """
    Vue AJAX pour supprimer une image d'annonce
    """
    try:
        image = get_object_or_404(AnnonceImage, id=image_id)
        
        # Vérifier que l'utilisateur est propriétaire de l'annonce
        if image.annonce.utilisateur != request.user:
            return JsonResponse({
                'success': False, 
                'error': 'Permission refusée'
            }, status=403)
        
        # Supprimer le fichier du storage
        if image.image and default_storage.exists(image.image.name):
            default_storage.delete(image.image.name)
        
        # Supprimer l'enregistrement de la DB
        image.delete()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)


@login_required
def handle_image_uploads(request, annonce, uploaded_files=None):
    """
    Fonction utilitaire pour traiter l'upload de nouvelles images
    """
    # Si pas de fichiers fournis, chercher dans request.FILES
    if uploaded_files is None:
        uploaded_files = request.FILES.getlist('imageUpload')
    
    if not uploaded_files:
        return
    
    current_image_count = annonce.images.count()
    max_images = 10
    
    # Vérifier le nombre total d'images
    if current_image_count + len(uploaded_files) > max_images:
        messages.warning(
            request,
            f'Limite de {max_images} images atteinte. '
            f'Seules {max_images - current_image_count} image(s) ont été ajoutées.'
        )
        uploaded_files = uploaded_files[:max_images - current_image_count]
    
    uploaded_count = 0
    # Traiter chaque image
    for image_file in uploaded_files:
        # Validation de la taille (5MB max)
        if image_file.size > 5 * 1024 * 1024:  # 5MB
            messages.warning(
                request,
                f'L\'image {image_file.name} est trop volumineuse (max 5MB).'
            )
            continue
        
        # Validation du format
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_extension = os.path.splitext(image_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            messages.warning(
                request,
                f'Format non supporté pour {image_file.name}. '
                f'Formats acceptés: JPG, PNG, GIF, WebP'
            )
            continue
        
        # Créer l'enregistrement de l'image
        try:
            AnnonceImage.objects.create(
                annonce=annonce,
                image=image_file
            )
            uploaded_count += 1
        except Exception as e:
            messages.error(
                request,
                f'Erreur lors de l\'upload de {image_file.name}: {str(e)}'
            )
    
    if uploaded_count > 0:
        messages.success(
            request,
            f'{uploaded_count} image(s) ajoutée(s) avec succès.'
        )

# Vue optionnelle pour l'upload AJAX d'images
@login_required
@require_POST 
def upload_annonce_images(request, annonce_id):
    """
    Vue AJAX pour uploader de nouvelles images
    """
    try:
        annonce = get_object_or_404(Annonce, id=annonce_id, utilisateur=request.user)
        
        if not request.FILES.getlist('images'):
            return JsonResponse({
                'success': False,
                'error': 'Aucune image fournie'
            })
        
        handle_image_uploads(request, annonce)
        
        # Retourner les nouvelles images
        images_data = []
        for image in annonce.images.all():
            images_data.append({
                'id': image.id,
                'url': image.image.url,
            })
        
        return JsonResponse({
            'success': True,
            'images': images_data,
            'total_images': len(images_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)





@login_required
def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(AnnonceImage, id=image_id, annonce__utilisateur=request.user)
        image.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def gerer_annonces(request):
    # ---- Stats ----
    total_annonces = Annonce.objects.count()
    annonces_en_attente = Annonce.objects.filter(statut="en_attente").count()
    annonces_approuvees = Annonce.objects.filter(statut="approuve").count()
    annonces_rejetees = Annonce.objects.filter(statut="rejete").count()

    # ---- Filtres ----
    annonces = Annonce.objects.all()
    statut = request.GET.get("statut")
    marque = request.GET.get("marque")
    prix_min = request.GET.get("prix_min")
    prix_max = request.GET.get("prix_max")
    date_creation = request.GET.get("date_creation")
    search = request.GET.get("search")

    if statut:
        annonces = annonces.filter(statut=statut)
    if marque:
        annonces = annonces.filter(marque__icontains=marque)
    if prix_min:
        annonces = annonces.filter(prix__gte=prix_min)
    if prix_max:
        annonces = annonces.filter(prix__lte=prix_max)
    if date_creation:
        annonces = annonces.filter(date_creation__date=date_creation)
    if search:
        annonces = annonces.filter(titre__icontains=search)

    # ---- Pagination ----
    paginator = Paginator(annonces.order_by("-date_creation"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # ---- Marques distinctes ----
    marques = Annonce.objects.values_list("marque", flat=True).distinct()

    context = {
        "total_annonces": total_annonces,
        "annonces_en_attente": annonces_en_attente,
        "annonces_approuvees": annonces_approuvees,
        "annonces_rejetees": annonces_rejetees,
        "annonces": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "paginator": paginator,
        "marques": marques,
    }
    return render(request, "admindash/gererannonces.html", context)


@login_required
def change_status(request, annonce_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")
            if new_status not in ["approuve", "rejete"]:
                return JsonResponse({"success": False, "message": "Statut invalide"})

            annonce = get_object_or_404(Annonce, id=annonce_id)
            annonce.statut = new_status
            annonce.save()
            return JsonResponse({"success": True, "message": f"Annonce {new_status} avec succès"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Méthode non autorisée"}, status=405)


@login_required
def bulk_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            annonces_ids = data.get("annonces", [])

            if action not in ["approve", "reject"]:
                return JsonResponse({"success": False, "message": "Action invalide"})

            new_status = "approuve" if action == "approve" else "rejete"

            annonces = Annonce.objects.filter(id__in=annonces_ids)
            updated_count = annonces.update(statut=new_status)

            return JsonResponse({
                "success": True,
                "message": f"{updated_count} annonce(s) {new_status} avec succès"
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Méthode non autorisée"}, status=405)





@login_required
def gerer_users(request):
    users = CustomUser.objects.all()
    
    total_users = users.count()
    total_moderators = users.filter(role="moderateur").count()
    total_admins = users.filter(is_superuser=True).count()
    
    return render(request, 'admindash/gererusers.html', {
        "users": users,
        "total_users": total_users,
        "total_moderators": total_moderators,
        "total_admins": total_admins,
    })


@require_POST
@login_required
def supprimer_utilisateur(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_superuser:
        return JsonResponse({"success": False, "message": "Impossible de supprimer un admin"})
    user.delete()
    return JsonResponse({"success": True})

@require_POST
@login_required
def changer_role_utilisateur(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Protection des super admins
    if user.is_superuser:
        return JsonResponse({
            "success": False, 
            "message": "Impossible de modifier le rôle d'un admin"
        })

    # Parse l'action
    data = json.loads(request.body)
    action = data.get("action")

    # Change le rôle
    if action == "promote":
        user.role = "moderateur"
        message = f"{user.username} est maintenant modérateur"
    elif action == "demote":
        user.role = "user"
        message = f"{user.username} est maintenant utilisateur"
    else:
        return JsonResponse({
            "success": False, 
            "message": "Action invalide"
        })

    user.save()

    # ✅ Le middleware s'occupe de rafraîchir les données
    return JsonResponse({
        "success": True,
        "message": message
    })
    
@login_required
def supprimer_annonce_admin(request, annonce_id):
    # Vérifier que l'utilisateur est admin
    if not request.user.role == 'admin':
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")

    annonce = get_object_or_404(Annonce, pk=annonce_id)

    if request.method == 'POST':
        # Supprimer les images
        for image in annonce.images.all():
            if image.image and default_storage.exists(image.image.name):
                default_storage.delete(image.image.name)
            image.delete()
        # Supprimer l'annonce
        annonce.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Annonce supprimée par admin'})
        else:
            messages.success(request, "Annonce supprimée par admin.")
            return redirect('gerer_annonces')  # nom de la vue liste pour admin

    # Si GET ou autre méthode
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect('gerer_annonces')
    








User = get_user_model()
@login_required
def forgot_password(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email_input = request.POST.get('identifier')

        # Validation
        if not email_input:
            return JsonResponse({
                "success": False,
                "message": "Veuillez entrer une adresse email."
            })

        # Vérifier que c'est bien l'email de l'utilisateur connecté
        if email_input != request.user.email:
            return JsonResponse({
                "success": False,
                "message": "Cet email ne correspond pas à votre compte."
            })

        user = request.user

        # Génère un code à 6 chiffres
        code = f"{random.randint(100000, 999999)}"

        try:
            from .models import PasswordResetCode
            
            # Supprime les anciens codes non utilisés pour cet utilisateur
            PasswordResetCode.objects.filter(user=user, is_used=False).delete()
            
            # Sauvegarde le nouveau code
            reset_code = PasswordResetCode.objects.create(
                user=user,
                code=code,
                verification_method='email'
            )
            
            print(f"✓ Code créé : {reset_code.code} pour {user.email}")  # Debug

            # Envoie le mail
            send_mail(
                subject="Votre code de réinitialisation",
                message=f"Bonjour {user.first_name or 'utilisateur'},\n\nVotre code de réinitialisation est : {code}\n\nCe code est valide pendant 10 minutes.\n\nSi vous n'avez pas demandé ce code, ignorez ce message.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            print(f"✓ Email envoyé à {user.email}")  # Debug

            return JsonResponse({
                "success": True,
                "message": "Le code a été envoyé sur votre email.",
                "redirect": reverse("verify_code")
            })
            
        except Exception as e:
            print(f"✗ ERREUR : {str(e)}")  # Debug détaillé
            import traceback
            traceback.print_exc()
            
            return JsonResponse({
                "success": False,
                "message": f"Erreur : {str(e)}"
            })

    return render(request, "pages/forgot_password.html")


@login_required
def verify_code(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        code_input = request.POST.get("code")
        
        if not code_input:
            return JsonResponse({
                "success": False,
                "message": "Veuillez entrer le code."
            })
        
        try:
            from .models import PasswordResetCode
            
            # Récupère le dernier code non utilisé pour cet utilisateur
            reset_code = PasswordResetCode.objects.filter(
                user=request.user,
                code=code_input,
                is_used=False
            ).latest('created_at')
            
            print(f"✓ Code trouvé : {reset_code.code}")  # Debug
            
            # Vérifie l'expiration (10 minutes)
            if not reset_code.is_valid():
                return JsonResponse({
                    "success": False,
                    "message": "Ce code a expiré. Veuillez demander un nouveau code."
                })
            
            # Marque le code comme utilisé
            reset_code.is_used = True
            reset_code.save()
            
            print(f"✓ Code validé pour {request.user.email}")  # Debug
            
            # Stocke une confirmation dans la session
            request.session['code_verified'] = True
            request.session['verified_at'] = timezone.now().isoformat()
            
            return JsonResponse({
                "success": True,
                "message": "Code vérifié avec succès !",
                "redirect": reverse("nvmdp")
            })
            
        except PasswordResetCode.DoesNotExist:
            print(f"✗ Code invalide : {code_input}")  # Debug
            return JsonResponse({
                "success": False,
                "message": "Code invalide. Veuillez vérifier et réessayer."
            })
        except Exception as e:
            print(f"✗ ERREUR verify_code : {str(e)}")  # Debug
            import traceback
            traceback.print_exc()
            return JsonResponse({
                "success": False,
                "message": "Une erreur est survenue."
            })

    return render(request, "pages/codeverif.html")


# ==================== ÉTAPE 3 : Changer le mot de passe ====================
@login_required
def nvmdp(request):
    # Vérifie que le code a été validé
    if not request.session.get('code_verified'):
        return redirect('forgot_password')
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validations
        if not new_password or not confirm_password:
            return JsonResponse({
                "success": False,
                "message": "Veuillez remplir tous les champs."
            })

        if new_password != confirm_password:
            return JsonResponse({
                "success": False,
                "message": "Les mots de passe ne correspondent pas."
            })
        
        if len(new_password) < 8:
            return JsonResponse({
                "success": False,
                "message": "Le mot de passe doit contenir au moins 8 caractères."
            })

        try:
            user = request.user
            user.set_password(new_password)
            user.save()
            
            # Maintient l'utilisateur connecté après changement
            update_session_auth_hash(request, user)
            
            # Nettoie la session
            request.session.pop('code_verified', None)
            request.session.pop('verified_at', None)
            
            print(f"✓ Mot de passe changé pour {user.email}")  # Debug

            return JsonResponse({
                "success": True,
                "message": "Mot de passe changé avec succès !",
                "redirect": "/"
            })
            
        except Exception as e:
            print(f"✗ ERREUR nvmdp : {str(e)}")  # Debug
            return JsonResponse({
                "success": False,
                "message": "Une erreur est survenue lors du changement."
            })

    return render(request, 'pages/nvmdp.html')


def test_email(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            send_mail(
                subject="Test Email Django 🚀",
                message="Bravo ! Si tu vois ce message, l'envoi d'email fonctionne correctement 🎉",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return JsonResponse({"success": True, "message": f"Email envoyé à {email}"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, "pages/test_email.html")



def test_sms_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        message_text = request.POST.get("message", "Message de test Twilio 🚀")
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=message_text,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            return JsonResponse({"success": True, "message": f"SMS envoyé à {phone}"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, "pages/test_sms.html")




@login_required
def annonces_list(request):
    # Toutes les annonces approuvées
    annonces = Annonce.objects.filter(statut='approuve')

    # Filtrage par recherche
    q = request.GET.get('q')
    if q:
        annonces = annonces.filter(titre__icontains=q)

    # Filtrage par marque
    marque = request.GET.get('marque')
    if marque:
        annonces = annonces.filter(marque=marque)

    # Filtrage par prix max
    prix_max = request.GET.get('prix_max')
    if prix_max:
        annonces = annonces.filter(prix__lte=prix_max)

    # Filtrage par année min
    annee_min = request.GET.get('annee_min')
    if annee_min:
        annonces = annonces.filter(annee__gte=annee_min)

    # Tri
    sort = request.GET.get('sort', 'recent')
    if sort == 'prix_asc':
        annonces = annonces.order_by('prix')
    elif sort == 'prix_desc':
        annonces = annonces.order_by('-prix')
    elif sort == 'km_asc':
        annonces = annonces.order_by('kilometrage')
    else:
        annonces = annonces.order_by('-date_creation')  # plus récentes

    # Pagination
    paginator = Paginator(annonces, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistiques
    total_annonces = Annonce.objects.filter(statut='approuve').count()
    total_marques = Annonce.objects.filter(statut='approuve').values('marque').distinct().count()
    total_vendeurs = Annonce.objects.filter(statut='approuve').values('utilisateur').distinct().count()
    # nouvelles annonces de cette semaine
    current_week = dt.now().isocalendar()[1]
    nouvelles_annonces = Annonce.objects.filter(
        statut='approuve',
        date_creation__week=current_week
    ).count()

    # Marques pour le select
    marques = Annonce.objects.filter(statut='approuve').values_list('marque', flat=True).distinct()

    context = {
        'annonces': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'total_annonces': total_annonces,
        'total_marques': total_marques,
        'total_vendeurs': total_vendeurs,
        'nouvelles_annonces': nouvelles_annonces,
        'marques': marques,
    }

    return render(request, 'pages/annonces.html', context)