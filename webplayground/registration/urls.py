from django.urls import path
# Importamos las vistas
from .views import SignUpView, ProfileUpdate, EmaillUpdate

urlpatterns = [
    path('signup/',SignUpView.as_view(), name="signup"),
    path('profile/',ProfileUpdate.as_view(), name="profile"),
    path('profile/email/',EmaillUpdate.as_view(), name="profile_email"),
    # Recuerda que el último path si lleva una , (coma) al final.

    # Acceder
    # accounts/ login/ [name='login']

    # Salir
    # accounts/ logout/ [name='logout']

    # Resetear contraseña desde el perfil de usuario.
    # accounts/ password_change/ [name='password_change'] 
    # Resetear contraseña desde el perfil de usuario. Template de realizado.
    # accounts/ password_change/done/ [name='password_change_done']

    # Resetear contraseña por correo, formulario de cambio de contraseña.
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm'] # Este es y es servido por ficheros. en la carpeta sent_emails
    # Resetear contraseña por correo, Mensaje de realizado con exito.
    # accounts/ password_change/done/ [name='password_change_done']
    # Resetear contraseña por correo, solicitud de correo
    # accounts/ password_reset/ [name='password_reset']
    # Resetear contraseña por correo, mensaje de envió de link para restauración de correo.
    # accounts/ password_reset/done/ [name='password_reset_done']
    
    
    # Registro de cuenta.
    # accounts/ signup/ [name='signup']

    # Página de perfil. 
    # accounts/ profile/ [name='profile']
    # accounts/ profile/email/ [name='profile_email']
]
