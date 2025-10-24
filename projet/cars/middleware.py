# votre_app/middleware.py
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from .models import CustomUser

class RefreshUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Stocker le rôle actuel AVANT toute modification
            session_role = request.session.get('user_role')
            
            # Récupérer les données à jour depuis la BDD
            try:
                db_user = CustomUser.objects.only('id', 'role', 'is_active').get(pk=request.user.pk)
            except CustomUser.DoesNotExist:
                logout(request)
                return redirect('login')
            
            # Si c'est la première fois, sauvegarder le rôle
            if session_role is None:
                request.session['user_role'] = db_user.role
                session_role = db_user.role
            
            # Comparer le rôle en session avec celui en BDD
            if session_role != db_user.role:
                # Le rôle a changé, déconnecter l'utilisateur
                logout(request)
                return redirect('login')
            
            # Mettre à jour le rôle en session
            request.session['user_role'] = db_user.role
            
            # Mettre à jour request.user avec les nouvelles données
            request.user.refresh_from_db()
            
            # Vérifier si le compte est actif
            if not request.user.is_active:
                logout(request)
                return redirect('login')
            
            # Protection des pages admin
            if request.path.startswith('/admindash/'):
                if request.user.role not in ['admin', 'moderateur']:
                    logout(request)
                    return redirect('home')
        
        return None