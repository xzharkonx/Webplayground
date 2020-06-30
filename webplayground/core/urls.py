from django.urls import path
from . import views
#Observa que ahora se importan las views de la app
from .views import HomePageView, SamplePageView

#Ahora se llaman de forma diferente porque son clases
urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('sample/', SamplePageView.as_view(), name="sample"),
]