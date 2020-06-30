from django.db import models
# Importamos el modelo de Usuario.
from django.contrib.auth.models import User

# importamos para agregar una señal al modelo thread
# La señal que ocuparemos será m2m_changed 
# Esto es para cuando el campo messages del modelo thread cambie
# DOCUMENTACIÓN: https://docs.djangoproject.com/en/2.0/ref/signals/#m2m-changed
from django.db.models.signals import m2m_changed

# Create your models here.

# Modelo de mensajes
class Message(models.Model):
    # Cargamos el usuario en modo cascada por si se borra el usuario, se borren
    # todos los mensajes que tiene...
    # Ponemos está busqueda en reversa related_name='messages' para saber cuantos
    # mensajes en total hay de un usuario en un hilo y así poder saber también
    # la fecha y hora del último mensaje que envio y mostrarlo en los Templates.
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario", related_name='messages')
    # Evidentemente no vamos a dejar que el usuario pueda borrar una instancia 
    # lo normal en esto casos es crear un campo 'active' que simule que se borra
    # pero en realidad solo lo dejará como desactivado en la base de datos, es una
    # posible solución.
    content = models.TextField(verbose_name="Contenido")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return str(self.user)

    class Meta: 
        verbose_name = "Mensajería"
        verbose_name_plural = "Mensajes"
        ordering = ['created']

# Model Manager de Thread
class ThreadManager(models.Manager):
    def find(self, user1, user2):
        # Desarrollamos un filtro, es muy facil porque
        # dentro de un método de un objectManager, la 
        # palabra self siempre hace referencia al propio
        # queryset que tiene todas las instancias de ese modelo
        # en nuetro caso Thread y se verá así
        # self equivale a  Thread.objects.all(), teniendo esto en cuenta
        # accedemos directamente a .filter  self.filter(users=user1).filter(users=user2)
        queryset = self.filter(users=user1).filter(users=user2)
        # Si la longitud de este queryset es mayor que 0 significa
        # que por lo menos hay un elemento que se ha encontrado
        # ocea un hilo, así que lo devolveremos
        if len(queryset) > 0:
            # El que tenemos en la primera posición.
            return queryset[0]  
        return None
        # Si no se ejecuta nunca, en última instancia devolveriamos
        # None, dando a entender pues que no se ha encontrado

    # Habiendo hecho esto teoricamente nuestro test ahora debería de
    # pasar la prueba, por que ya hemos desarrollado el metodo
    # fin que se llama así en test:
    # Thread.objects.find(self.user1,self.user2)

    def find_or_create(self, user1, user2):
        # self equivale a  Thread.objects.all()
        # Buscará si los 2 usuarios que creamos
        # se encuentran en el hilo.
        thread = self.find(user1,user2)
        # Si no los encuentra los creará
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1,user2)
        # retornaremos el hilo cargado de usuarios
        return thread


# Modelo de Hilo de mensajes
class Thread(models.Model):
    # El related_name='threads' le ponemos ese nombre para poder 
    # acceder comodamente desde un User, haciendo un user.threads
    # para una "Búsqueda inversa" y traer todos los hilos a los 
    # que pertenece.
    users = models.ManyToManyField(User, related_name='threads')
    # Le pasamos el modelo Message y almacenaría todos los mensajes
    # que forman parte del hilo.
    messages = models.ManyToManyField(Message)
    # Por tanto tendríamos un lugar como un punto de encuentro que
    # almacena los usuarios y los mensajes que escribiran esos usuarios

    # Se creará un campo llamado update
    # De esta forma se detectará cuando se modifico por última vez un hilo
    # y nos permitirá hacer un ordenamiento automatizado de todas estás 
    # conversaciones.
    updated = models.DateTimeField(auto_now=True)

    # Llamamos al Thread Manager para crear nuestros filtos personalizados
    # que hemos creado dentro de está funsión
    # Estos se llaman en base a la función que se necesite como 
    # por ejemplo: Thread.objects.find()
    objects = ThreadManager()

    class Meta:
        verbose_name = "Hilo"
        verbose_name_plural = "Hilos"
        # No funcionará el ordenamiento.
        ordering = ['-updated']
        # La clave está en que los campos m2m no afectan directamente al updated
        # ellos se gestionan aparte, nosotros somos quienes tenemos que forzar el guardado
        # para que se almacene en update la fecha de modificación, esta es cla clave de todo.
        # En que momento sabemos que se añaden o se dejan de añadir mensajes a un hilo y como
        # podemos forzar está actualización aunque sea simbolica del modelo Thread pues 
        # lo haremos en la señal que habiamos creado messages_changed


# Para crear la señal lo haremos de está forma alternativa:
# primero crearemos la funsión con la que queremos trabajar
# se llamará "messages" respecto al campo que vamos a estár al pendiente
# de que cambie en el modelo thread y añadimos _changed
def messages_changed(sender, **kwargs):
    # Primero recuperamos 3 cosas:
    # 1.- La instancia que está mandando la señal (es decir, el hilo al que
    # estamos intentando añadir nuestros mensajes)
    # 2.- La acción que se está ejecutando, por que está señal tiene varias
    # acciones(por ejemplo detecta el pre_add o el post_add), nosotros 
    # queremos detectar el pre_add que es el momento justo antes de añadir
    # los mensajes ( y el post_add es el momento despues de añadirlos).
    # 3.- Y también necesitamos pk_set que hace referencia a un conjunto
    # que almacena los identificadores de todos los mensajes que se
    # van a añadir dentro de está relación m2m.
    # Para recuperarlos lo haremos  a partir del diccionario **kwargs.pop()
    # que saca el elemento del diccionario y dento de pop() le pasaremos
    # la "instance" y si no la encuentra que devuelva None por defecto,
    # la "accion" y el "pk_set"
    # Para más detalle revisar la documentación: https://docs.djangoproject.com/en/2.0/ref/signals/#m2m-changed
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    # Cuando los hayamos recuperado, vamos a debuguearlos con un print.
    print(instance, action, pk_set)
    # LA clave de todo esto es interceptar el pk_set, buscar los
    # mensajes que contiene a partir de estás claves primarias
    # y si su autor, es decir el usuario que los ha creado no forma
    # parte del hilo que tenemos aquí en instance borrarlos para
    # que no se añadan (la instancia del modelo Thread con los 
    # nuevos datos recogitos en este caso en el test)
    # Lo haremos abajo...
    # De momento crearemos esta tupla para almacenar esos usuarios
    # que no están registrados en el hilo y que si están en los mensajes
    # que será los "usuarios espia"
    false_pk_set = set()
    # Primero que nada comprobamos si la acción es 'pre_add'
    # antes de guardar los datos. La interceptaremos y 
    # borraremos los mensajes de pk_set
    if action == 'pre_add':
        # Con un for comprobaremos todos los msg_pk que hay en el conjunto
        # pk_set
        for msg_pk in pk_set:
            # Aquí recuperaremos los mensajes por la pk recabada de msg_pk
            # de cada item en la lista pk_set que recuperamos.
            msg = Message.objects.get(pk=msg_pk)
            # Ahora para cada mensaje haremos la comprobación con un if
            # si el autor de un mensaje  no se encuentra dentro de los
            # usuarios que hay añadidos en la instancia del hilo.            
            if msg.user not in instance.users.all():
                # podríamos mostrar un mensaje debug para saber que usuario
                # no forma parte de la instancia
                print("Ups, ({}) no forma parte del hilo".format(msg.user))
                # Podemos haber hecho:
                # pk_set.remove(msg_pk)
                # pero al hacerlo, mientras está en el for lo eliminará y
                # cambiará la longitud, al hacer esto nos dará este error
                # pero podemos corregirlo almacenando estos usuarios en una
                # tupla y luego removerlos.

                # Por ello haremos lo siguiente:
                # Habiendo creando una variable de tipo tupla arriba...
                # Almacenamos a esos usuarios en nuestra tupla que creamos para
                # almacenar a esos "usuarios espia" que no están en nuestro hilo
                false_pk_set.add(msg_pk)
    
    # Eliminaremos a esos "usuarios espias"
    # Se buscarían los mensajes que sí están en pk_set y los borramos de pk_set
    # estos que se borren serán la diferencia, es decir que no esten pk_set y que
    # si están en false_pk_set
    pk_set.difference_update(false_pk_set)

    # Forzar la actualización haciendo un save
    # Haciendo a la referencia de instance y asu metodo .save() nosotros podemos
    # guardar de forma simbolica aun que no haya ocurrido ningún cambio el modelo
    # Eso actualizará nuestro campo updated y así reaccionará el ordenamiento
    # de mensajes por el último enviado en /messenger/
    # Está instancia es del hílo, es decir, que en vez de crearce solo se guardará
    # y al guardarse, está mofigicará su fecha para así ordenarse al principio.
    instance.save()

# Para llamarsa solo haremos lo siguiente:
# le pasamos la señal que queremos conectar (la funsión)
# y el sender en nuestro caso seria: nombre_del_modelo.nombre_del_campo.through
# Así conectaremos la señal con cualquier campo m2m de messages
m2m_changed.connect(messages_changed, sender=Thread.messages.through)

# Si corremos nuestros test ya estarán validados si hacer ninguna modificación en el TEST
# Lo que hemos hecho es interceptar el pk_set y borrar cuyos autores no forma parte del hilo
# por que en el test se declarana un usuario espia.
# Así que esto es TDD en toda la regla por que a fuerza de refactorizar, hemos conseguido
# validar un test sin alterar su estructura. En el archivo test.py.