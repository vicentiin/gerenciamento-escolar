"""
Módulo de Views do projeto principal (pontesParaoFuturo).

Este módulo contém a view da página inicial da aplicação.
"""

from django.http import HttpResponse  # type: ignore
from django.shortcuts import render, redirect
from django.urls import reverse


def pagina_inicial(request):
    """
    Exibe a página inicial da aplicação.

    Metodos HTTP:
    - GET: Renderiza a página inicial com link para login
    - POST: Retorna mensagem de erro (método não suportado)

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML inicial ou mensagem de erro

    Contexto:
    - go_to_login: URL para página de login (reversa de 'usuarios:login')
    """
    if request.method == "GET":
        go_to_login = reverse('usuarios:login')
        data = {'go_to_login': go_to_login}
        return render(request, 'inicio.html', data)
    else:
        return HttpResponse('Algo errado ou novo')
