"""webplayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Para una búsqueda en reversa de la app pages
from pages.urls import pages_patters
# Para cargar imagenes.
from django.conf import settings
# Para la app profiles
from profiles.urls import profiles_patterns
# Para la app messenger
from messenger.urls import messenger_patterns

urlpatterns = [
    path('', include('core.urls')),
    # path('pages/', include('pages.urls')),
    path('pages/', include(pages_patters)),
    path('admin/', admin.site.urls),

    # Paths de Auth (Autenticación, Login - Logout).
    # Importamos de esta forma para incluir la autenticación de django
    # y django nos provera de distintas urls para la autenticación.
    path('accounts/', include('django.contrib.auth.urls')),
    # Para poder registrar usuarios
    path('accounts/', include('registration.urls')),
    # Paths de profiles
    path('profiles/', include(profiles_patterns)),
    # Paths de messenger
    path('messenger/', include(messenger_patterns)),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)