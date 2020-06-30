# Nuestro objetivo es proporcionarle al menos 3 campos para
# proporcinarle en su perfil.
# - Una imagen como Avatar.
# - Un texto como biografía.
# - Un link para que pueda colocar un enlace a una página web.

# Podriamos crear un modelo de usuario para estos 3 campos extra pero esa seria la solución compleja.
# Lo simple sería crear un modelo Profile que contenga estos 3 campos y una relación de 1 a 1 con un usuario,
# de manaera que cada instancia de User tenga enlazada una de Profile.

# Se crea aquí, por que en lugar de crear una nueva App, por defecto Django al identificarse el usuario lo 
# redireccionaba a  'accounts/profile', pues por esta razón, si lo gestiona ahí lo vamos a manejar dentro de 
# esta App registration.

# Más adelante se creará una App 'profile' para los perfiles publicos, pero está parte privada la vamos a manejar
# en registration

from django.db import models
# Importamos el modelo de usuario.
from django.contrib.auth.models import User
# Importamos un decorador para decorar una función que nos permita crear un perfil automaticamente.
from django.dispatch import receiver
# Importamos para que al guardar post_save, esta señal ejecute la función. hay varias funciones como antes
# de guardat, eliminar, etc...
# Más info hasta abajo de este script o en: https://docs.djangoproject.com/en/2.0/topics/signals/
from django.db.models.signals import post_save, pre_save

# Función para hacer que la imagen antigua de perfil se borre si se cambia.
# recibira instance y filename.
# instance hace referencia al objeto que se está guardando pero despues de que hayamos confirmado el nuevo valor
# es decir si nosotros vamos a la instancia y comprobamos el valor de avatar "ya saldrá en nuevo valor
# de avatar que hemos puesto".
# Y en filename tendríamos pues el nombre del fichero con la imagen que queremos sobreescribir (imagen.jpg)
# Por tanto el truco consiste en recuperar la antigua instancia haciendo un old_instance
# SOLO ELIMINARÁ LA IMÁGEN SI SE CAMBIA, PERO SI SE BORRA, NO LA BORRARA. =C
def custom_upload_to(instance, filename):
    # De está forma habremos recuperado la instancia del modelo perfil justo como estaba antes de guardarla y tal como se pasa 
    # aquí a instance
    old_instance = Profile.objects.get(pk=instance.pk)
    # Ya solo accederiamos a esa instancia y conseguiriamos eliminarla automáticamente.
    # Consultar los comentarios en: https://www.udemy.com/course/curso-django-2-practico-desarrollo-web-python-3/learn/lecture/9899228#questions/7064996
    old_instance.avatar.delete()
    # Si no funcionará por la versión de Django, prodría funcionar con está:
    # old_instance.avatar.delete(save = False)

    # Ya solo devolvemos la url de la nueva imagen, habrá que indicarla al devolver el método y sepa
    # que nombre darle al guardarlo.
    return 'profiles/'+ filename # La url que se completará será /profiles/imagen.jpg

# Create your models here.
class Profile(models.Model):
    # Aquí harémos la relación con el modelo User
    # Será una relación 1 a 1
    # Le pasaremos el modelo User (la tabla de usuarios), lo que hará cuando se elimine ese usuario
    # se elimine también su perfil (osea el objeto de este modelo enlazado a ese objeto del modelo User).

    # Le indica al modelo que solo puede haber un perfil por cada usuario, es decir, no se pueden tener
    # 2 perfiles para un mismo usuario ni distintos usuarios para un mismo perfil (esta es la clave del ONE TO ONE).
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos que tendrá nuestro modelo para nuestro usuario.
    # Cargamos la imagen con las configuraciones arriba de la funsión.
    # Más info para upload_to en: https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField.upload_to
    # Podemos hacer un monton de cosas como darles diferentes nombres, crear automátimente directorios a partir de fechas, etc...
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    
    # Se añade para que al listar (mostar) los campos del modelo Profile se ordenen por nombre de usuario en 'profiles:list'
    class Meta:
        ordering = ['user__username']

    # Optimizando las imagenes. Crearemos una función que nos permita eliminar todas las imagenes
    # de perfil que se cambian y que se quedan guardadas porque solo mostarán la foto actual de perfil.
    # Aquí que recuperaremos el antiguo avatar y lo borraremos haciendo uso de un metodo llamado delete
    # que tienen los ImageField y los FileField y una vez que lo hayamos borrado, pues devolveremos la 
    # ruta normal a profiles


# RELACIONES ENTRE MODELOS.
    # En Django tenemos 3 tipos de relaciones.

# - OneToOneField, (1:1) 1 usuario - 1 perfil
    # Relación de Uno a Uno, única para ambos sentidos.
    # Un Usuario un Perfil, un Perfil un Usuario.

# - ForeignKeyField, (1:N) 1 autor <- N entradas
    # Para claves foraneas.
    # Relación de Uno a N, de Uno a Varios, única en un solo sentido.
    # Un Autor en Entradas.
      
# - ManyToManyField, (N:M) N entradas <-> M categorías
    # Relación N a M, de Varios a Varios.
    # Es no única en ningun sentido.
    # Las N entradas pueden estar relacionadas con M categorías.
    # O viceversa.

# El primer detalle que vamos a solucionar es la prevención de un potencial error que podría hacer tambalear
# toda nuestra página y ese es el momento de crear un perfil tal y como lo tenemos ahora.
# Siempre que un usuario se registre y se identifique será redireccionado directamente a su perfil de
# manera que éste se creará con la instancia enlazada si no existe.
# Pero qué ocurriría si por alguna razón el usuario se registra y no accede nunca.
# Pues que nos quedará un usuario sin perfil una situación tendiente a errores en el futuro así que vamos
# a solucionar esto introduciendo algo muy interesante conocido como Signals Señales una señal es un disparador
# que se llama automáticamente después de un evento que ocurre en nuestro O.R.M en nuestro caso lo que
# haremos es crear automáticamente un perfil justo después de que se crea un usuario y así estaremos cien
# por cien seguros de que todos los usuarios cuentan con un perfil desde el primer momento creará una
# señal es relativamente fácil se puede hacer en el propio fichero Models de nuestra aplicación 

# De vuelta a nuestro código vamos a abrir el fichero models.py para definir una señal la podemos
# crear como una función en la parte de abajo y la vamos a llamar de esta forma ensure_profile_exists

# Se llama así porque tiene sentido porque se va a encargar de confirmar
# que el perfil siempre existe. Está función va a recibir una variable llamada sender (recibira el modelo)
# una llamada instance (la instancia del modelo que le pasamos User al modelo Profile) y los **kwargs que los pasaremos así.
# Entonces está funsión se disparará luego de que un usuario de guarde. 
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    # Si existe está clave llamada 'created' es la primera vez que se guarda está instancia por tanto se acaba
    # de crear y para asegurarnos que únicamente vamos a entrar a este if la primera vez, vamos a
    # devolver por defecto false si no existe esta entrada en el diccionario.
    print("CREANDO LA INSTANCIA DE PERFIL POR PRIMERA VEZ")
    if kwargs.get('created',False): 
        # Hacemos lo siguiente para asegurarnos de crear una 
        # instancia de perfil si está no existe y le vamos a pasar de user la instance.
        Profile.objects.get_or_create(user=instance)
        # Incluso podemos mostrar un mensaje.
        print("Se acaba de crear un usuario por primera vez y su perfil de enlazado")

# Ahora solo tenemos que llamar está señal para ello la decoraremos importando arriba llamada receiver
# y poder añadir la funcionalidad

# Esto es un decorador que nosotros vamos a definir justo encima
# de nuestra señal y dentro tenemos que pasarle dos cosas el primer lugar el tipo de la señal que queremos
# configurar tenemos señales para hacer referencia al momento justo antes de guardar una instancia o justo
# después de guardarla o justo antes de borrarla o justo después de borrarla.

# Estos tipos de señales reciben nombres como post_migrate pre_save post_save pre_delete y post_delete.
# En nuestro caso necesitamos que el usuario exista.
# Por tanto tenemos que hacerlo después de que se cree y por tanto necesitamos utilizar una llamada post.
# Después de guardarse.
# Pero claro está no existe.
# Tenemos que importarla y la vamos a importar de django.db.models.signals import post_save
# fijaros que hay varios tipos.

# https://docs.djangoproject.com/en/2.0/topics/signals/

# Después de que se guarde el usuario ya sólo nos falta indicarle cuál es el modelo que tiene que enviar
# la señal y que lo haremos indicando aquí el Sender y el nombre del modelo y User por tanto lo que estamos
# configurando en todo este código es una señal que no es más que una función que ejecuta un código en
# un momento determinado de la vida de una instancia ya sea antes de guardarla después o antes de borrarla
# o después que nuestro caso es después de guardarla.

#
# Solución a borrar la imagen y borrar el archivo también. Función creada por Mi.
#

# Lo que pasa es que al hacer click en borrar la imagen, la interfaz borra la 
# dirección de la imagen pero no borrará la imagen del almacenamiento, así
# que declararemos esta señal (signal) para que al indicarle con pre_save
# (antes de guardar) vea si la imagen viene vacía, si es así buscará en la 
# old_instance la url anterior de la imagen que estaba (si estaba) y si la 
# encuentra la borrará.

# Al final del archivo models.py de la app registration añadir lo siguiente :
# Está funsión se dispará antes de salvar los datos en el modelo perfil.        
@receiver(pre_save, sender=Profile)
def custom_delete_avatar(sender, instance, update_fields=None, **kwargs):
    # Se coloca dentro de un try por que al crear el usuario no encuentra
    # un perfil para ese usuario por lo tanto si no lo encutra
    # no hara nada.
    # Y siempre que se cree un usuario o antes de guardarse dará error 
    # por que no habrá aún un perfil, y este no se creará por que dará este error.
    # de que no encuentra el perfil
    try: # Extraido de: https://www.it-swarm.dev/es/python/comprobar-si-existe-un-objeto/1067877124/
        # Si encuentra el perfil es que ya se acreado antes el usuario
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        # Si no existe es porque apenas se va a registrar el usuario y al momento
        # de registrarse se crea una instancia automáticamente pero antes de que se cree
        # entrará aquí y dará error porque no recupera nada es por eso que le indicamos
        # a la instancia sea none, para que no nos de error al no encontrarla.
        old_instance = None
    # Si es que hay un perfil podremos comprobar si su avatar viene vació, esto es para
    # saber si va a borrar la imagen y no se acargado nada.
    if old_instance:
       # print("Encontro un pefil")
        if instance.avatar  == "":
            print("Borrando la imagen.")
            old_instance.avatar.delete()
    else:
        print("No encontro un pefil, se creará en breve")

# Faltaría revisar si al  eliminar el perfil se eliminará la imagen... 
# URL info: https://www.udemy.com/course/curso-django-2-practico-desarrollo-web-python-3/learn/lecture/9899228#questions/6523236
# https://github.com/un1t/django-cleanup

# Como dice ahí lo que prodríamos hacer sería instalar Django Cleanup
#      pip install django-cleanup
# Luego lo agregaremos al archivo settings y agregamos a las apps la siguiente:
# INSTALLED_APPS = (
#     ...,
#     'django_cleanup.apps.CleanupConfig',
# )

# Sigue las instrucciones simplemente pip install y agrégalo al final de las app instalada y wuala borrara todos los archivos media
# que estén relacionados con dicho modelo / instancia.
# Ya se comprobo y si funciono, así que añadirlo.
# Se recomienda revisar más de la documentación.