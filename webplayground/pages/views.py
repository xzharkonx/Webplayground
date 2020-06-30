#Para las FBV (Vistas Basadas en Funciones)
#from django.shortcuts import render, get_object_or_404, get_list_or_404

#Para una lista de CBV
from django.views.generic.list import ListView
#Para un solo elemento CBV
from django.views.generic.detail import DetailView
#Para insertar los datos
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#Para redireccionar a una página
from django.urls import reverse, reverse_lazy
#Para redireccionar si no estamos autenticados
from django.shortcuts import redirect
#Importamos para poder decorar las funciones
from django.utils.decorators import method_decorator
#Importamos decorador que nos indicara si estamos autenticados o no
from django.contrib.admin.views.decorators import staff_member_required

from .models import Page
#Aquí cargamos el formulario para poder editarlo
from .forms import PageForm

# Create your views here.

#Mixin de autorización
#Se puede sobre escribir cualquier atributo o metodo, por lo que son muy útilies.
class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro del staff
    """
    # dispatch: envió
    # request: solicitud
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_staff:
    #         return redirect(reverse_lazy('admin:login'))
    #     return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

    #Se eliminan las lineas de comprobación y se coloca el decorador
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

    #Existen 3 tipos:
    # staff_member_required
        ## Solo miembros del staff
    # login_required
        ## Solo para identificar que el usuario tenga acceso.
    # permission_required
        ## Que el usuario tenga algun tipo de permiso especial.
    
    # Ventajas:
    # La ventaja que tiene es que al acceder y no estar logueado o no tener ese permiso
    # nos redireccionará al login pero, al acceder, este nos redireccionara a la página
    # que en un principio queriamos entrar.

    # También nos evita de hacer mixins y poder crear los decoradores directamente
    # pero en este caso, se creo el decorador dentro del mixin.

    # Tambien nos ayudan para no heredarlas en las clases (los mixins) y solo colocar
    # el decorador y del metodo que se quiere realizar las primeras acciones antes de
    # acceder a la logíca de la vista(la clase) y retornar el template.

    # Al colocar el decorador, nos evitamos de copiar tantes veces la comprobación del usuario.

    # por lo regular se coloca a las paginas: create, update y delete.

    # También podemos decorar desde el archivo urls para que desde ahí gestione, para ello
    # y de todo lo de más se coloca documentación abajo.

    ## Algo que debemos investigar es que nos redirecciona a http://localhost:8000/admin/login/?next=''
    ## por lo que estaría bien saber como hacer que en vez que nos redireccione ahí, nos redireccione
    ## a {% url 'login' %}.
    ## Podríamos usar la primera opción de autenticación que teniamos al principio y probar.
    
    #Documentación:
    # https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator
    # https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-permission-required-decorator
    # https://docs.djangoproject.com/en/2.0/_modules/django/contrib/admin/views/decorators/
    # https://docs.djangoproject.com/en/2.0/topics/class-based-views/intro/#decorating-class-based-views

#Vistas Basadas en Clases
#ListView
#Para cuando tengamos que devolver una lista de las instancias de un modelo.

# El nombre generico que deberá tener de nuestro template (html) y del la lista de objetos
# que tenemos que recorrer en nuestro template para ver esos items sera: page_list
# tomando primero el nombre del modelo seguido de _list para listarlos.
class PageListView(ListView):
    model = Page

#FBV
# def pages(request):
#     pages = get_list_or_404(Page)
#     return render(request, 'pages/pages.html', {'pages':pages})

#DetailView
#Para cuando tengamos que devolver una única instancia de un modelo, es decir
# un solo objeto del modelo.

# El nombre generico que deberá tener de nuestro template (html) sera: page_detail
# tomando primero el nombre del modelo seguido de _detail para el nombre del template.
# Y del objeto que tenemos que tener en nuestro template para ver ese item es el
# propio nombre del modelo: page, solo accederemos a sus atributos que querramos poner.

class PageDetailView(DetailView):
    model = Page

# def page(request, page_id, page_slug):
#     page = get_object_or_404(Page, id=page_id)
#     return render(request, 'pages/page.html', {'page':page})

#PageCreate
#Para cuando queramos insertar datos de nuestros modelos
#Colocamos el decorador en vez de heredarle StaffRequiredMixin
@method_decorator(staff_member_required, name="dispatch")
class PageCreate(CreateView):
    model = Page
    #Aquí cargamos el formulario importado el que se podrá editar
    #Al configurarlo así, se podrá cargar.
    form_class = PageForm
    #Como el form_class ya incluye estos campos podemos quitar
    #los fields aquí
    #fields = ['title', 'content','order']
    #Pero no funcionara así
    #success_url = reverse('pages:pages')
    #Tenemos que utilizar un metodo llamado get_success_url
    #para retornar el nuevo valor, entonces hay que hacer una
    #redifinición.
    # def get_success_url(self):
    #     return reverse('pages:pages')

    #Pero los creadores de django pensaron en una reimplementación
    #más fácil a todo esto sin get_success_url, para esto crearon reverse_lazy
    success_url = reverse_lazy('pages:pages')

    #Ahutorización a una sección
    #Aquí podremos saber que usuario es
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_staff:
    #       si no es correcto no nos direccionara al login  
    #       return redirect(reverse_lazy('admin:login'))
    #     si el permiso es correcto servimos la página
    #     return super(PageCreate, self).dispatch(request, *args, **kwargs)
    #Esto debería ser para todas las páginas pero se utilizará un mixin.

#PageUpdate
#Para cuando queramos actualizar datos de nuestros modelos.
#Colocamos el decorador en vez de heredarle StaffRequiredMixin
@method_decorator(staff_member_required, name="dispatch")
class PageUpdate(UpdateView):
    model = Page
    #Aquí cargamos el formulario importado el que se podrá editar
    #Al configurarlo así, se podrá cargar.
    form_class = PageForm
    #Como el form_class ya incluye estos campos podemos quitar
    #los fields aquí
    #fields = ['title', 'content','order']
    #Para utilizar otro formulario, le pasamos ese
    #sufijo por defecto, esto para indicarle el template
    #como el sifijo de create es page_form.html, el de update
    # será page_update_form.html
    template_name_suffix = '_update_form'
    #Si queremos que nos reedirija a la misma página
    #pero mostrando los datos ya actualizados
    #Este success_url no funcionara 
    #success_url = reverse_lazy('pages:pages')
    #No tenemos más remedio que redifinir el get_success_url
    #para acceder a self y de esta forma al objeto
    #pero con reverse_lazy
    #De esta manera recreamos la url a la que le estaríamos
    #pasando la id del objeto y sepa cual actualizar
    #Y le mandamos una variable diciendole que todo esta bien
    #con '?ok'
    def get_success_url(self):
        return reverse_lazy('pages:update',args=[self.object.id]) + '?ok'

#PageDelete
#Para cuando queramos eliminar datos de nuestros modelos.
#Colocamos el decorador en vez de heredarle StaffRequiredMixin
@method_decorator(staff_member_required, name="dispatch")
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')