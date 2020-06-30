from django.urls import path
#Para las FBV (Vistas Basadas en Funciones)
#from . import views
#Para las CBV (Vistas Basadas en Clases)
from .views import PageListView, PageDetailView, PageCreate, PageUpdate, PageDelete

#Busqueda en reversa, 
pages_patters = ([
    path('', PageListView.as_view(), name='pages'),
    #path('<int:page_id>/<slug:page_slug>/', PageDetailView.as_view(), name='page'),
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('create/', PageCreate.as_view(), name='create'),
    path('update/<int:pk>/', PageUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PageDelete.as_view(), name='delete'),
], 'pages')

# urlpatterns = [
#     path('', PageListView.as_view(), name='pages'),
#     #path('<int:page_id>/<slug:page_slug>/', PageDetailView.as_view(), name='page'),
#     path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
# ]