# Se crea este formulario para hacer el Email obligatorio al registrarse.
from django import forms
# Podemos hacer un formulario desde 0 y utilizarlo o
# Extender el UserCreationForm
# hacemos lo secundario ya que nos ahorrará tiempo y haremos menos.
#Importamos un formulario ya hecho por django para gestionar
#los registros de los usuarios
from django.contrib.auth.forms import UserCreationForm
# Se importa el modelo de usuario para que se pueda guardar en la base de datos.
from django.contrib.auth.models import User
# Se importa el modelo de perfil para que se pueda guardar en la base de datos.
from .models import Profile

#
# Configuraciones para editar nuestro formulario de registro a partir de 
# las configuraciónes default de Django de User
#

# Aquí vamos a extender (heredar) del formulario de UserCreationForm.
# Luego lo obtendremos en la view para procesar el formulario.
class UserCreationFormWithEmail(UserCreationForm):
    # Creamos un nuevo campo llamado email.
    # Este campo esta en el modelo User.
    # Estos valores son los que tiene este campo por default el modelo User.
    email = forms.EmailField(required=True, help_text='Obligatorio, 254 caracteres como máximo y también debe ser valido')
    # Este campo antes no se había tomado en cuenta, solo usuario password y confirmación de password, por lo que hacerlo
    # así, es como si le estuvieramos diciendo que también considere recabar el Email, esto se puede hacer porque este campo está dentro
    # del modelo User, por lo que no se puede añadir algún otro campo a no ser que este dentro del modelo.

    # Si quisieramos editar el texto de ayuda (help_text) tendremos que debugear el codigo de la página para ver que campos aparecen
    # y así poder editarlos, es lo que se me ocurre ahora mismo.

    class Meta:
        # Le indicamos el modelo.
        model = User
        # Le pasamos una tupla para indicarle que campos tendrá el formulario.
        # Añadiendole el campo email que antes no mostraba por default.
        fields = ('username', 'email', 'password1', 'password2')
        # Esto funcionara porque 'email' ya es un campo de user. Si no exitiera no funcionaría.
        # Por lo que se le añade un filtro para que lo utilice.

    # Transformamos el campo de email en un campo único.
    # Es decir, para que no se vuelva a repetir cuando se registre un usuario.
    # Para hacerlo, añadimos esta validación especifica de campo.

    # Definimos una función que obligatoriamente iniciará con clean_ y luego
    # el nombre del campo que querramos validar si no lo ponemos así no funcionaría.
    def clean_email(self):
        # Así podremos recuperar el email que estamos validando.
        # Así recuperaremos el valor que tiene clean al momento de enviar el formulario.
        email = self.cleaned_data.get('email')
        # Comprobamos que este email no exista en la base de datos.
        # Esto nos devolvera uno o varios emails (objetos del modelo).
        # Devolvera un queryset o lista vacia si no encuentra ningun elemento.
        # si encuentra un email entrará en la condición y lanzará un error.
        # Así ya no se registrará este email y pedirá registrar otro.
        if User.objects.filter(email=email).exists():
            # Lanzamos un error si encontro un email igual al que se ha colocado.
            # La función acabaría y devolverá el error.
            raise forms.ValidationError("El email ha sido registrado, prueba con otro.")
        # Si se devuelve el email, el campo ha sido validado correctamente.
        return email

    # Para editar el formulario se pone lo siguiente.
    # Se edita en las views.py en tiempo real y no aquí en forms.py, en la clase UserCreationFormWithEmail
    # del archivo vires.py dentro de la clase Meta y declarando los widgets. 
    # Por que si no, las validaciones que ya hay hechas por default se machacarían por lo que  
    # lo editamos aquí en tiempo real.

#
# Configuraciones para editar nuestro formulario de perfil.
#

class ProfileForm(forms.ModelForm):

    # Aquí irian los campos creados por nosotros, pero como ya estamos ocupando un modelo
    # es como si ya los hubieramos creado, por lo que solo se ocupa la clase Meta para
    # editar los estilos de un formulario ocupando el modelo ya creado.

    class Meta:
        # Importamos el modelo
        model = Profile
        # Le indicamos los campos que queremos editar.
        fields = ['avatar', 'bio', 'link']
        # Establecemos los whidgets para editar los estilos y configuraciones del formulario.
        widgets = {
            # Este widget es el de la imagen y es el que muestra la dirección de la imagen y el cuadrito
            # para limpiar la imagen
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3','rows':3, 'placeholder':'Biografía','style':'max-height:300px;min-height:100px;'}),
            'link': forms.URLInput(attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),
        }

#
# Creación de Formulario para unicamente hacer la edición de email desde el perfil de usuario
#

class EmailForm(forms.ModelForm):
    # Reutilizamos el campo email de la clase UserCreationFormWithEmail para que lo considere
    email = forms.EmailField(required=True, help_text='Obligatorio, 254 caracteres como máximo y también debe ser valido')

    class Meta:
        model = User
        fields = ['email']

        # Justo debajo podríamos colocar los widgets pero no tendría sentido porque el User ya es un modelo que tiene sus 
        # propias validaciones también internas, la unica  forma de redifinir los widgets sin cargarnos todas esas 
        # validaciones es hacerlo en tiempo de ejecución, por tanto acabaremos de motar el widget del email ya en la propia vista.

    # Pero necesitamos validar el correo, que sea aptimo, así que copiamos el validador que teniamos arriba de UserCreationFormWithEmail.
    # Pero la validación anterior no nos funcionara bien por que está validación lo que hace es comprobar si existe  un email con esa
    # dirección antes de guardarlo y como el email del usuario ya existia desde el principio siempre lo va a encontrar, por tanto esta
    # validación no la podemos hacer de esta forma. Lo que tenemos que comprobar es si este email se ha modificado, si el campo email
    # ha cambiado significa que se a añadido un nuevo email, entonces si que tiene sentido hacer está comprobación.
        
    # Transformamos el campo de email en un campo único.
    # Es decir, para que no se vuelva a repetir cuando se registre un usuario.
    # Para hacerlo, añadimos esta validación especifica de campo.

    # Definimos una función que obligatoriamente iniciará con clean_ y luego
    # el nombre del campo que querramos validar si no lo ponemos así no funcionaría.
    def clean_email(self):
        # Así podremos recuperar el email que estamos validando.
        # Así recuperaremos el valor que tiene clean al momento de enviar el formulario.
        email = self.cleaned_data.get('email')

        # Comprobamos si el email se ha modificado.
        # self.changed_data Que es una lista que almacena todos los campos que se han editado en el formulario.
        # Si dentro de  está lista no se encuentra el nombre 'email' significa que  ese campo no se ha modificado,
        # pero si lo encuentra, es que se ha modificado y por tanto tiene sentido de que hagamos la comprobación
        # de que ese email si exista
        if 'email' in self.changed_data: 
        # La validación de abajo que comprueba si existe se coloca dentro.
        # Y como el email se a cambiado, por tanto es nuevo, así que no entra en la
        # validación de abajo que dice que si encuentra un email, este lanzará un error.

            # Comprobamos que este email no exista en la base de datos.
            # Esto nos devolvera uno o varios emails (objetos del modelo).
            # Devolvera un queryset o lista vacia si no encuentra ningun elemento.
            # si encuentra un email entrará en la condición y lanzará un error.
            # Así ya no se registrará este email y pedirá registrar otro.
            if User.objects.filter(email=email).exists():
                # Lanzamos un error si encontro un email igual al que se ha colocado.
                # La función acabaría y devolverá el error.
                raise forms.ValidationError("El email ha sido registrado, prueba con otro.")
        # Si se devuelve el email, el campo ha sido validado correctamente.
        return email