from django import forms
from .models import Page
#Para personalizar el formulario
#Como vamos a crear un formulario que está enlazado 
#a un modelo, no hace falta que lo creemos desde cero
#si no que podemos enlazarle el modelo para que se genere automaticamente.
#Para ello importamos el modelo page.
class PageForm(forms.ModelForm):
    #No necesitamos agregar campos aquí
    #por que no estamos creando los campos del formulario
    #si no que los estamos jalando del modelo.
    class Meta:#Como las vistas basadas en clase
        #Le enlazamos el modelo
        model = Page
        #Creamos un campo para indicarlo al usuario que editar
        fields = ['title', 'content', 'order']
        #Aquí editamos las propiedades del formulario con los widgets
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título'}),

            #importa los plugins de ckeditor en el template en caso de usarlo.
            #https://github.com/django-ckeditor/django-ckeditor#outside-of-django-admin

            #Para hacer que el campo de ckeditor sea adaptativo y también para poder
            #inyectar código css. Revisar siguiente url y ver un archivo
            #en pages/static/pages/css/custom_ckeditor.css
            #https://gist.github.com/hcosta/15ae0835e5824685d46e75f49efc1bcb
            #E inyectarlo en el template, revisar:
            #pages/templates/pages/includes/pages_menu.html
            #Y ahora también inyectarlo en admin.py de nuestra app pages
            #Deberemos reiniciar la app.

            #El 'placeholder':'Contenido' quizá no funcione por ckeditor 
            'content': forms.Textarea(attrs={'class':'form-control','placeholder':'Contenido'}),
            'order': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Orden'}),
        }  

        #Ahora para cambiar el nombre de las etiquetas de los campos de entrada
        #en el formulario lo haremos con labels.

        labels = {
            #Se dejaran sin nombre.
            'title':'','content':'','order':''
        }