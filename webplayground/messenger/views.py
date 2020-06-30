from django.shortcuts import render
# Con algunos datos ya creados como 1 hilo y varios mensajes
# ahora crearemos las vistas
# Necesitamos por lo menos 2 vistas.
# Una para mostrar los hilos de un usuario.
# Y otra para mostrar un hilo en concreto con la 
# conversación.
# Por lo que debemos crear 2 vistas.

# Un ListView para listar todos los hilos de un usuario.
# Una DetailView para listar todos los mensajes de un hilo.
# Pero esta ListView ya no se ocupo
# from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Se cambio ListView por TemplateView
from django.views.generic import TemplateView

# Importamos el modelo de usuarios para crear hilos de conversación.
from django.contrib.auth.models import User
from .models import Thread, Message

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Importamos para retornar el error y para trabajar con archivos json
from django.http import Http404, JsonResponse
# Importamos para buscar un objeto o devolver un error si no lo encuentra.
# Importamos el redirect para redireccionarnos a la lista de mensajes de ese hilo
from django.shortcuts import get_object_or_404, redirect
# Importamos para redireccionar de forma peresosa
from django.urls import reverse_lazy

# Create your views here.
# Con el ListView
# No podemos dejarla así por que en el caso de la ListView
# lo que estamos devolviendo aquí son todas las instancias
# que existen de la clase Thread pero nosotros queremos filtrarlas
# y unicamente devolver las del usuario que esta identificado
# Le ponemos el @method_decorator y el login_required para 
# asegurarnos de que este logueado
# @method_decorator(login_required, name="dispatch")
# class ThreadList(ListView):
    # model = Thread

    # Para filrar un queryset por defecto lo que podemos hacer es volver a 
    # definir el metodo get_queryset

    # def get_queryset(self):
    #     # Ahora lo que haríamos sería recuperar el propio queryset llamando
    #     # a la superclase y haciendo un .get_queryset() de forma que en un
    #     # queryset tendríamos todas las instancias de thread (porque esto es el comportamiento generico)        
    #     queryset = super(ThreadList, self).get_queryset()
    #     # Sin embargo nosotros queremos devolverla filtrada así que haremos un return de este queryset
    #     # haciendo un filter users y haciendo referencia a self.request.user y filtrariamos por el usuario
    #     # que está identificado en este momento.
    #     # Pero si vamos a hacerlo debemos asegurarnos de que al menos un usuario a iniciado la sesión
    #     # así que lo que vamos a hacer es importar el decorador de login_required y el @method_decorator
    #     # Recuerda importar lo necesario.
    #     return queryset.filter(users=self.request.user)

# Pero nuestro caso es especial, porque tenemos una relación inversa donde a partir del usuario podemos
# consultar todos los hilos haciendo un user.thread.all() de está forma en el template. 
# Por tanto todo lo que hemos hecho no nos hace falta, simplemente es otra forma de hacerlo porque no lo necesiamos.
# Directamente en el propio template ya podremos consultar todos los hilos del usuario, en su lugar simplemente
# vamos a declarar un TemplateView y hacemos lo de abajo.

@method_decorator(login_required, name="dispatch")
class ThreadList(TemplateView):
    template_name = "messenger/thread_list.html"

# Respecto a está DetailView ya la tenemos bien
# El único problema que surgiría es si un usuario pone en su barra un identificador de un hilo
# del cual no forma parte y podría haberlo, por tant tenemos que filtrar el hilo y devolver el 
# error en caso de que no forme parte de el. 
# Vamos que el usuario solo pueda ver los hilos de los que forma parte.
@method_decorator(login_required, name="dispatch")
class ThreadDetail(DetailView):
    model = Thread

    # Así que en este caso en lugar de sobreescribir el get_queryset que hicimos antes
    # sobreescribiriamos un get_object que es el metodo correlativo al Detail (porque
    # unicamente manejamos una instancia)
    def get_object(self):
        # Recuperamos el objeto actual con super para simular que recuperamos el objeto
        obj = super(ThreadDetail, self).get_object()
        # Comprobamos si el usuario que está identificado no se encuentra entre todos
        # los usuarios que forman parte del hilo
        if self.request.user not in obj.users.all():
            # Si no se enceuntra le mandaríamos un error de 404
            raise Http404()
        return obj

# Con esto ya estaría, solo tendríamos que configurar las urls

# Creando el Chat
# VBF para los mensajes asincronos con javascript
def add_message(request, pk):
    # print(request.GET)
    json_response = {'created':False}
    # Devolvemos la respuesta en formato json
    # Recuerda enviar las credenciales por javascript en el fetch junto a la url
    if request.user.is_authenticated:
        # Recuperamos el contenido (Es la variable content que declaramos y se la enviamos por la url)
        content = request.GET.get('content', None)
        # Si hay contenido recuperaremos el hilo con la pk de la funsión que le pasamos.
        if content:
            # Recuperamos el hilo y lo instanciamos
            thread = get_object_or_404(Thread, pk=pk)
            # Creamos un mensaje
            message = Message.objects.create(user=request.user, content=content)
            # Añadimos el mensaje al hilo
            # Esto automaticamente utilizando la señal previamente creada
            # validará que el autor forma parte del hilo, si no nos lo añadira
            thread.messages.add(message)
            # ahora
            json_response['created'] = True

            # Se agrego esta funcionalidad despues que lo que hace es que si iniciamos
            # una conversación con un usuario nuevo, lo que haremos será redireccionarnos
            # automaticamente 
            # Detectamos si hay mensajes del hilo
            if len(thread.messages.all()) is 1:
                # Si tiene un mensaje, crearíamos una nueva clave llamada 'first'
                json_response['first'] = True
                # Devolveremos True si solo hay un mensaje en la conversación
    else:
        raise Http404("User is not authenticated")
    
    return JsonResponse(json_response)

#
# Vista para crear los hilos de conversación
#
# Crearemos una vista, tomaremos el request y el username con el que queremos empezar a
# charlar.
@login_required
def start_thread(request, username):
    # Recuperamos el usuario que le pasamos
    user = get_object_or_404(User, username=username)
    # Creamos el hilo  le pasamos los usuarios.
    # Con request.user, este usuario (el usuario logueado que inicio la conversación)
    # Y user es el usuario al que queremos iniciar la conversación
    thread = Thread.objects.find_or_create(user, request.user)
    # Retornamos a la vista enviando por los argumentos la pk de este hilo creado
    print(thread.pk)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))