from django.urls import path
from .views import ProfileListView, ProfileDetailView

profiles_patterns = ([
    path('', ProfileListView.as_view(), name='list'),
    # Aquí le indicamos la url del perfil seleccionado a partir de su nombre.
    path('<username>/', ProfileDetailView.as_view(), name='detail'),
], "profiles")
