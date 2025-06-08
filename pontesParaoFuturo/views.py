from django.http import HttpResponse #type: ignore
from django.shortcuts import render, redirect
from django.urls import reverse



def pagina_inicial(request):
    if request.method == "GET":
        go_to_login = reverse('usuarios:login')
        data = {'mensagem': 'Estou aqui!', 'go_to_login': go_to_login}
        return render(request, 'inicio.html', data)
    else:
        return HttpResponse('Algo errado ou novo')