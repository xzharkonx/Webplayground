# Eliminamos está por que no la necesitaremos...
# from django.shortcuts import render
# Importamos un formulario generico ya hecho por django para gestionar
# los registros de los usuarios
# from django.contrib.auth.forms import UserCreationForm
# Ya no se importa aquí, porque ya se a importado en forms.py con una nueva configuración.
# Por lo que ahora cargamos el formulario de forms.py. Hacerlo de esta forma nos permitirá
# configurar y añadir un campo de Email y poder recuperar nuestra cuenta de Email.
# El nuevo formulario que hemos creado con estás configuraciones se llama UserCreationFormWithEmail

# También importaremos de forms.py el formulario ProfileForm que tiene las nuevas configuraciones
# de estilos para nuestro formulario del perfil.

from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Para poder modificar el formulario e importar los widgets.
from django import forms

# Cargamos el TemplateView para los datos del Perfil de Usuario.
# from django.views.generic.base import TemplateView
# Ya no se ocupo TemplateView por que se reemplazo por UpdateView
# para actualizar los datos del Perfil de usuario
from django.views.generic.edit import UpdateView

# Importamos el nuevo modelo creado de Perfiles.
from .models import Profile

# Importamos para autenticar al usuario
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

#Con esta CBV podremos indicar un formulario de registro para nuestra app
class SignUpView(CreateView):
    # Ya no se importa aquí, porque ya se a importado en forms.py con una nueva configuración.
    # form_class = UserCreationForm
    # Por lo que ahora cargamos el formulario de forms.py.
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'
    # No se puede aplicar success_url:
    # success_url = reverse_lazy('login')
    # ya que vamos a concatenar una variable llamada register para saber si
    # al redireccionar a template de login, nos hemos registrado correctamenete.
    def get_success_url(self):
        return reverse_lazy('login') + '?register'
        # Recuerda recibir está variable en el template

    # Para editar el formulario se pone lo siguiente.
    # Primero revisamos el formulario generado automaticamente para saber que campos tieme
    # y saber como editarlo.
    # Se edita aquí en tiempo real y no en forms.py en la clase UserCreationFormWithEmail
    # dentro de la clase Meta y declarando los widgets. Por que si no, las validaciones 
    # que ya hay hechas por default se machacarían por lo que  lo editamos aquí en tiempo real.
    def get_form(self,form_class=None):
        # Se va a ejecutar para obtener el formulario
        # así que obtenemos el propio metodo y lo ejecutamos.
        # Entonces se habrá modificado en tiempo real.
        form = super(SignUpView, self).get_form()
        # Recuerda importar arriba a from django impor forms para acceder a los tipos de formularios
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        # Se añadio el campo email que antes no mostrabamos al cargar el modelo, ahora ya se a validado y cargado desde
        # el archivo .forms con UserCreationFormWithEmail
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Dirección Email.'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repite la contraseña'})
        # Se puede modificar el label también así:
        # form.fields['username'].label = ''
        # Pero en nuestro caso solo se oculto desde el template con css: display:none
        # Para hacerlo menos tedioso y que el codigo de arriba este menos redundante.

        # Y también deberiamos añadir al archivo base.html una url 'signuo' para mostrar un boton de registro si
        # no estamos autenticados.
        return form


# Necesitaremos crear una página para editar el perfil, por ahora se creará como un simple templateView
# Luego se explicara el porque, ahora solo es de ejemplo para ver que todo funcione bien...(se explica al final de este texto).
# Recuerda importar el TemplateView
# Este template ProfileUpdate solo se verá si está autenticado, por lo que hay que importar ciertas 
# librerías arriba para autenticar a los usuarios en estás vistas.
# Se le indicará que requiere estar autenticado.
# Al final se cambiará a UpdateView para actualizar los datos del Perfil de usuario
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    # Recuerda que el modelo Profile tiene un campo OneToOne con el modelo User.
    # es necesario recuperarlo para saber de quien serán los datos del perfil.

    # Model ya no se utilzó porque lo cargamos del form_class y este
    # asu vez cargará el formulario que hemos creado y este ya carga el 
    # modelo, por lo que ya no es necesario declararlo aquí.
    # model = Profile

    # Le indicamos los campos que queremos mostrar.
    # Pero como creamos un formulario en el archivo forms.py, importaremos
    # el formulario y de ahí los campos por lo que lo de abajo ya no se
    # utilizará
    # fields = ['avatar', 'bio', 'link']

    # En este formulario cargamos el modelo y editamos los estilos del
    # formulario.
    form_class = ProfileForm


    # Al actualizar los datos, le indicaremos que vuelva a cargar el perfil.
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    # Ahora para que funcione la gran pregunta...
    # ¿Como vamos a conseguir el identificador o la pk del perfil para poder 
    # editarlo y enviarlo a esta UpdateView?

    # Contestando con otra pregunta,
    # ¿Crees que sería buena idea pasar una pk del perfil en el path?
    # Pues obviamente la respuesta es no... por que si hicieramos eso, cualquiera
    # podría editar los perfiles de los otros usuarios solo sabiendo el ID.
    
    # ¿Además si todavia no hemos creado una instacia (es decir capturar los datos
    # que envien desde el formulario) del perfil como vamos a mostrar
    # un formulario para editarlo?.

    # Por suerte, aun que no sepamos el id del perfil, siempre podemos saber el ID del
    # usuario autenticado sin necesidad de pasarlo en el path porque este se almacena en
    # la propia request, así pues hay que recuperar de alguna forma el perfil a partir de
    # este identificador del usuario que hay en request.
    # ¿Como vamos a hacer está mágia oscura?, pues es muy facil por que las UpdateVire tienen
    # un metodo llamado  get_object que podemos sobreescribir para recuperar el objeto 
    # que se va a editar. Y lo vamosa recuperar de Profile.objects.get(user=self.request.user)

    def get_object(self):
        # Recuperar el objeto que se va a editar (el User).
        # return Profile.objects.get(user=self.request.user)
        # Hacerlo así nos dara un error de:
        # Profile matching query does not exist.
        # Y es que estamos tratando de recuperar un profile que todavía no existe.
        # Debemos asegurarnos de que exista antes de poder devolverlo para poder editarlo en el formulario.
        # Por lo que el metodo .get se sobreescribe por .get_or_create()
        # Lo que hace es conseguir o crear, es decir, busca a partir de este filtro (user=self.request.user)
        # que nosotros le damos y si no lo encuentra lo crea.(recuerda que user es un campo del modelo).
        # Lo malo es que no podemos crearlo y recuperarlo directamente, porque esto devuelve una tupla 
        # formada por el propio objeto que estamos recuperando o editando que es Profile en este caso y
        # una variable de tipo booleano donde almacena si se a creado o no en este momento (create)
        # tenemos que hacerlo así.
        # Y una vez tenemos el perfil, lo podemos devolver.
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
        # Ahora ya se podra cargar el formulario.
        # Se podrá enviar y guardar los datos, pero como obviamente al guardarlos nos redireccionara
        # a la misma vista con los datos rellenos, pero la foto de perfil no la cargara... 
        # ¿Porque pasará esto?...

        # No es que tengamos un error ni nada, es solo que no hemos configurado el formulario para
        # aceptar ficheros desde el propio html. Y es que tenemos que configurar el formulario de 
        # una forma especifica. Habrá que ir a profile_form.html

#
# Vista para lanzar el formularió y poder editar el email de perfil.
#

@method_decorator(login_required, name='dispatch')
class EmaillUpdate(UpdateView):

    # En este formulario cargamos el modelo y editamos los estilos del
    # formulario.
    form_class = EmailForm
    # Al actualizar los datos, le indicaremos que vuelva a cargar el perfil.
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # Modificaremos este metodo pero ya no para recuperar el perfil, si no 
        # para recuperar el usuario, por lo que solo lo devolveremos de la request
        return self.request.user

    # Así que ahora nos faltarían los editar el formulario con los widgets desde ahí
    # para que los cargue en tiempo de ejecución porque el modelo User (usuario)  ya 
    # tiene sus propios validadores y sus propios widgets, así que los sobreescribimos aquí.

    def get_form(self, form_class=None):
        # Se va a ejecutar para obtener el formulario
        # así que obtenemos el propio metodo y lo ejecutamos.
        # Entonces se habrá modificado en tiempo real.
        form = super(EmaillUpdate, self).get_form()
        # Se añadio el campo email que antes no mostrabamos al cargar el modelo, ahora ya se a validado y cargado desde
        # el archivo .forms
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Dirección Email.'})
        return form