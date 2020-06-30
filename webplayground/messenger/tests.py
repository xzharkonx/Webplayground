from django.test import TestCase

# Importamos los modelos con los que trabajaremos.
# Importamos el modelo User
from django.contrib.auth.models import User
# Importamos los modelos que creamos.
from .models import Thread, Message

# INDICACIONES
# Podemos hacer el Test deteniendo el servidor y ejecutando el comando:
# python manage.py test nombre_app
# en nuestro caso: python manage.py test messenger
# pero también podemos ejecutar unsa sola serie de test declarando la clase
# python manage.py test menssenger.tests.ThreadTestCase
# Incluso solo podríamos ejecutar un solo Test incluyendo el nombre de la
# función del test:
# python manage.py test menssenger.tests.ThreadTestCase.test_add_users_to_thread


# Create your tests here.

# Creamos una clase con un nombre cualquiera para los Test
# En este caso la llamaremos ThreadTestCase y heredaremos de TestCase
class ThreadTestCase(TestCase):
    # Inicializamos todas las variables e instancias y con lo que
    # Vayamos a trabajar en setUp
    def setUp(self):
        # Creamos 2 Usuarios
        self.user1 = User.objects.create_user('user1',None,'test1234')
        self.user2 = User.objects.create_user('user2',None,'test1234')
        self.user3 = User.objects.create_user('user3',None,'test1234')

        # Creamos un hilo (un objeto vacio de la forma del modelo Thread en .models)
        self.thread = Thread.objects.create()

        # Listo para poder añadirle los usuarios y los mensajes.

    # Con esto tenemos el entorno de pruebas, así que podemos empezar a crear
    # algunos test siempre que empiecen estos con la palabra test_

    # Test sencillo que nos permitira añadir usuarios.
    def test_add_users_to_thread(self):
        # Tomamos los usuarios y los insertamos a users por que es una lista
        # de usuarios dentro del modelo thread
        self.thread.users.add(self.user1,self.user2)
        # Consultamos todos los usuarios dentro del hilo y si son los 2
        # entonces es que se hab creado e insertado correctamente.
        # De esta manera comprobamos que se ha hecho de manera correcta
        self.assertEqual(len(self.thread.users.all()),2)
    
    # Hacemos un test para saber si se creo un hilo y si existe
    # buscandolo por filtros, filtrando por los usuarios que pertenecen
    # a ese hilo.
    def test_filter_thread_by_users(self):
        # Por medio de self accedemos al objeto que declaramos en setUp
        # y este es del tipo Thread (osea del mismo modelo) y le pasamos
        # 2 objetos de tipo user.
        self.thread.users.add(self.user1,self.user2)

        # Recuperamos el hilo a partir de los 2 usuarios.
        # Con esto ya tendríamos todos los hilos donde
        # forma parte el usuario 1.
        # threads = Thread.objects.filter(users=self.user1)
        # Pero como podemos añadir un segundo filtro para filtrar
        # donde está el usuario 1 y además está el usuario 2.
        # pues añadimos otro filtro despues.
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        # esto podemos hacerlo por que al fin y al cabo no deja de ser un queryset
        # y como es un queryset podemos añadirle otro filtro y podemos añadirle
        # tantos como quisieramos.
        
        # A esto se referia cuando solo puede habrer un hilo con 2 usuarios D=

        # Así que luego de hacer estos filtros habremos recuperado el hilo donde están 
        # estos dos usuarios y si esto es verdad podremos comprobarlo haciendo lo siguiente:
        self.assertEqual(self.thread, threads[0])

    # Comprobamos un test que esta vacio y que solo se ha creado
    def test_filter_non_existent_thread(self):
        # Observa que no insertamos los usuarios.
        # Esto nos devolverá un queryset vació, es decir, con 0 hilos.
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        # así que hacemos una serción para comprobar que no se ha recuperado ningún hilo
        self.assertEqual(len(threads),0)

    # test para unos mensajes de prueba
    # Para comprobar si se puede añadir un mensaje a un hilo y si esté se ha añadido
    # correctamente como habíamos hecho con los usuarios
    def test_add_messages_to_thread(self):
        # Le añadimos al hilo los usuarios
        self.thread.users.add(self.user1, self.user2)
        # Creamos un mensaje y le pasamos un usuario y el mensaje.
        message1 = Message.objects.create(user=self.user1, content="Muy buenas")
        message2 = Message.objects.create(user=self.user2, content="Hola hola!")
        self.thread.messages.add(message1,message2)
        self.assertEqual(len(self.thread.messages.all()),2)

        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))

    
    # Con estos test hemos comprobado una serie de cosas.
        # La creación de los hilos.
        # La asignación de usuarios.
        # La recuperación de hilos a partir de los usuarios.
        # La creación de mensajes, la asignación a los hilos y la recuperación.

    # Ahora para que esto se considere TDD crearemos codigo y refactorizaremos
    # hasta conseguir validar algunos test.

    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content="Muy buenas")
        message2 = Message.objects.create(user=self.user2, content="Hola hola!")
        # El nuevo usuario que no está registrado en el hílo.
        message3 = Message.objects.create(user=self.user3, content="Soy un espía")
        self.thread.messages.add(message1,message2,message3)
        # El detalle es que si inserta el mensaje con ese usuario no registrado
        # y al consultarse, puede que de error por que no encontrará a ese
        # usuario por que no pertenece a la lista de usuarios enlazados a este hilo.
        # Si se hiciera len == 3 entonces si aceptaría el dato, pero al consultarse
        # podría dar error por que al buscar el mensaje con ese id no estará.
        self.assertEqual(len(self.thread.messages.all()), 2)
        # Para correguir este error, se verificará que solo los usuarios que
        # esten dentro de la lista de usuarios del hilo puedan crear los mensajes
        # esto sería como refactorízar el código de tal manera que arreglemos estos
        # errores.
        
        # Para esto utilizaremos una señal llamada change en el archivo models.py
        # de está app

    # Crearemos un Model Manager
    # El motivo de crearlo, será para crear nuestras funsiones personalizadas
    # que podamos ejecutar del modelo, en nuesto caso creamos la función .find()
    # para el modelo Thread en models.py
    # Haremos este test para probarlo con una nueva fución que añadiremos.
    def test_find_thread_with_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1,self.user2)
        # Con la función .find que hemos creado nos ahorramos de
        # hacer mucho filtro como:
        # threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        # y con esto habremos creado está función .find. para ver como es
        # revisar en modes.py el modelo Thread
        self.assertEqual(self.thread, thread)

    # Haciendo uso del Model Manager
    # Crearemos otra funsión como la de arriba pero en está ocación será buscarlo
    # y si no lo encuentra, que lo cree.
    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1,self.user2)
        self.assertEqual(self.thread, thread)    
        thread = Thread.objects.find_or_create(self.user1,self.user3)
        self.assertIsNotNone(thread)  
        
# Para probar, podemos acceder a la shell con:
# python manage.py shell
# e importamos los modelos.