from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static




urlpatterns= [
    path('',views.home,name='home'), 
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register,name='register'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('profile',views.profile,name='profile'),
    path('ajouterannonce',views.ajouter_annonce,name='ajouterannonce'),
    path('mesannonces',views.mesannonces,name='mesannonces'),
    path('annonce/<int:annonce_id>/', views.detail_annonce, name='detail_annonce'),
    path('chat', views.chat, name='chat'),
    path('annonce/supprimer/<int:annonce_id>/', views.supprimer_annonce, name='supprimer_annonce'),
    path('annonce/modifier/<int:annonce_id>/', views.edit_annonce, name='edit_annonce'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path("admindash/annonces/", views.gerer_annonces, name="gerer_annonces"),
    path("admindash/annonces/<int:annonce_id>/change-status/", views.change_status, name="change_status"),
    path("admindash/annonces/bulk-action/", views.bulk_action, name="bulk_action"),
    path('admindash/gererusers/', views.gerer_users, name='gerer_users'),
    path('admindash/supprimer-utilisateur/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('admindash/changer-role-utilisateur/<int:user_id>/', views.changer_role_utilisateur, name='changer_role_utilisateur'),
    path('admindash/supprimer-annonce/<int:annonce_id>/', views.supprimer_annonce_admin, name='supprimer_annonce_admin'),
    path('change_password/', views.change_password, name='change_password'),
    path('supprimermoncompte/', views.supprimermoncompte, name='supprimermoncompte'),
    path('parametres/', views.parametres, name='parametres'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('nvmdp/', views.nvmdp, name='nvmdp'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('test-email/', views.test_email, name='test_email'),
    path('test-sms/', views.test_sms_view, name='test_sms'),
    path('annonces/', views.annonces_list, name='annonces_list'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)