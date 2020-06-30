#importamos la clase para trabajar con las CBV (Vistas basadas en clase)
from django.views.generic.base import TemplateView
#Se mantiene render para poder reenviar el contexto.
from django.shortcuts import render

#Para llamar al template ahora se implementará una clase
class HomePageView(TemplateView):
    template_name = "core/home.html"

    #Este metodo lo sobreescribimos para pasarle el contexto de la forma
    #parecida a las FBV (Vistas Basadas en Funciones)
    #Se le pasa la petición, el nombre del template (ocea el mismo) y 
    #el contexto que le querramos pasar al template.
    #por lo general estos métodos se les pasa los paramétros que tiene.
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title':'Mi super Web Playground'})

class SamplePageView(TemplateView):
    template_name = "core/sample.html"



#Se desechan estas Vitas Basadas en Funciones
#Esta es una vista basada en funcion FBV
# def home(request):
#     return render(request, "core/home.html")

# def sample(request):
#     return render(request, "core/sample.html")