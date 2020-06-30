from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.

class ProfileTestCase(TestCase):
    # El este método es donde tenemos que preparar la prueba
    def setUp(self):
        # Lo único que tenemos que hacer es crear un usuario de pruebas.
        # create_user es un método que tiene el modelo User que es especial
        # porque nos permite pasarle una contraseña y el la encriptara automáticamente
        # Y le pasaremos un user, un email y una contraseña
        # (Como si crearamos un usuario).
        User.objects.create_user('test', 'test@test.com', 'test1234')
        # Entonces tenemos la preparación hecha y en esté punto ya se creará este usuario de
        # pruebas llamado test

    # Aquí tenemos la propia prueba cuyo nombre puede ser cualquiera
    # siempre que empiece con test_
    def test_profile_exists(self):
        # Ahora lo que tenemos que hacer aquí, que se ejecutará despues de que se creé el usuario
        # es comprobar si en Profile.objects hay un user igual a test y haremos un .exist() para que
        # nos devuelva un true o false.
        exists = Profile.objects.filter(user__username='test').exists()
        # Y como en toda prueba normal tenemos que ejecutar el testkeys haciendo lo siguiente...
        # Comparando que exist debe de tener si o sí el valor True.
        self.assertEqual(exists, True)

# Para ejecutar este test lo que hay que hacer es detener el servidor y ejecutar el siguiente comando:
# python manage.py test registration

# Con está prueba nos permitirá comprobar o corroborar que despues de crear un usuario, se acreado
# automaticamente un perfil enlazado a el.

# Más apuntes https://github.com/hcosta/curso-python-udemy/blob/master/Fase%204%20-%20Temas%20avanzados/Tema%2016%20-%20Documentaci%C3%B3n%20y%20Pruebas/Lecci%C3%B3n%2004%20(Apuntes)%20-%20Unittest.ipynb

# Recuerda que para hacer está prueba tuve un problema de acceso a la base de datos por lo que es recomendable hacer el test con la
# db.sqlite3 en vez de nuestra base de datos, a no ser de que configuremos los accesos para un user 'default'