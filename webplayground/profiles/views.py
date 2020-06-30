from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from registration.models import Profile


# Create your views here.
# Listamos del modelo perfil los perfiles
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # Si queremos hacer una páginación de datos, es decir,
    # mostrar cierta cantidad de datos de cierto modelo.
    # Agregamos el variable paginate_by y le asignamos un número
    # entero donde estableceremos el número de registros por página
    # que queremos mostrar.
    paginate_by = 9
    # Entonces cargaremos solo la primera página con 3 valores.
    # Para cargar las demás páginas agregaremos debajo de nuestro template
    # profile_list.html la páginación, así que lo siguiente es ir ahí
    # a colocarlo.

# Listamos un perfil del modelo Profile y lo mostramos
# recuperando por la url el username para saber
# que perfil es el que enviaremos
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        # En el template le pasaremos el username por que se listarán los objetos
        # del modelo Profile, solo habrá que pasarle el nombre de ese usuario
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
