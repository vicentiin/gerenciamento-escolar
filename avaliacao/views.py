"""
Módulo de Views para Gerenciamento de Avaliações e Notas.

Este módulo contém as vistas para:
- Cadastro de avaliações com vinculação a turmas-disciplinas
- Registro de notas de alunos em avaliações
- Suporte a requisições AJAX para seleção dinâmica de turmas

Tipos de operações:
- GET: Exibição de formulários
- POST: Processamento e persistência de dados
- AJAX: Retorno de dados em JSON
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from django.contrib import messages
from .forms import (
    AvaliacaoForm,
)
from usuarios.models import (
    Professor,
    Aluno,
)
from turmas.models import (
    Turma_Disciplina,
    Turma,
)
from .models import (
    Avaliacao,
    Nota,
)

# Create your views here.


def cadastro_avaliacao(request):
    """
    Realiza o cadastro de novas avaliações.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de avaliação
    - POST: Processa o cadastro validando duplicatas por período e data

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Não pode haver duas avaliações no mesmo período letivo e data de aplicação
    - Arquivo é opcional

    Campos:
    - titulo: Nome da avaliação
    - descricao: Descrição da avaliação
    - arquivo: Arquivo anexado (opcional)
    - status: Status da avaliação
    - turma_disciplina: Lista de turmas-disciplinas onde a avaliação será aplicada
    - data_aplicacao: Data de aplicação
    - periodo_letivo: Período letivo
    """
    if request.method == "GET":
        form = AvaliacaoForm()
        data = {'form': form, 'form_action': reverse(
            'avaliacao:cadastro_avaliacao')}
        return render(request, 'cadastros_avaliacoes/cadastro_avaliacao.html', data)
    else:
        # Coleta dados do formulário
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        arquivo = request.FILES.get('arquivo')
        status = request.POST.get('status')
        turma_disciplina = request.POST.getlist('turma_disciplina')
        data_aplicacao = request.POST.get('data_aplicacao')
        periodo_letivo = request.POST.get('periodo_letivo')

        # Verifica se já existe avaliação nesse período e data
        avaliacao_cadastrada = Avaliacao.objects.filter(
            periodo_letivo=periodo_letivo, data_aplicacao=data_aplicacao).first()
        if avaliacao_cadastrada:
            return HttpResponse('Avaliação nesse período já aplicada!')
        else:
            form = AvaliacaoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

            return HttpResponse('dados enviados')


@login_required(login_url='/auth/login/')
def cadastro_nota(request):
    """
    Realiza o registro de notas de alunos em avaliações.

    Metodos HTTP:
    - GET: Exibe formulário com seleção dinâmica de avaliação e turma
    - POST: Processa o registro de notas para múltiplos alunos

    Args:
        request (HttpRequest): Objeto de requisição HTTP contendo:
        - GET: 'valor' (parâmetro de query para avaliação selecionada)
        - POST: 'turma_numero', 'valor' (avaliação), 'aluno_X' e 'nota_X'

    Returns:
        HttpResponse: Página HTML com formulário (GET), JSON para AJAX, ou redirecionamento (POST)

    Fluxo:
    1. GET: Recupera avaliações do professor e turmas relacionadas
    2. Se AJAX: Retorna turmas e avaliação em JSON
    3. Exibe lista de alunos da turma selecionada
    4. POST: Processa registro de notas em lote
    5. Cria registros Nota para cada aluno com sua pontuação

    Suporte a AJAX:
    - Requisições com header 'X-Requested-With: XMLHttpRequest' retornam JSON

    Requer autenticação e usuário associado a um Professor
    """
    if request.method == "GET":
        try:
            # Obtém o professor associado ao usuário logado
            professor = Professor.objects.get(user=request.user)
        except Professor.DoesNotExist:
            return HttpResponse('Usuário não associado a um professor')

        # Consulta todas as avaliações do professor
        avaliacoes = Avaliacao.objects.filter(
            turma_disciplina__professor=professor
        ).values_list('titulo', flat=True).distinct()

        # Processa a avaliação selecionada
        av_choice = request.GET.get('valor')
        turmas_da_avaliacao = []

        if av_choice:
            # Obtém as turmas para a avaliação selecionada
            turmas_da_avaliacao = Turma.objects.filter(
                turma_disciplina__avaliacao_turma_disciplina__titulo=av_choice,
                turma_disciplina__professor=professor
            ).distinct().values_list('numero', flat=True)

        # Verifica se é requisição AJAX e retorna JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'turmas': list(turmas_da_avaliacao),
                'avaliacao': av_choice
            })

        # Recupera as turmas em que o professor leciona
        turmas = Turma_Disciplina.objects.filter(professor=professor).values_list(
            'turma__numero', flat=True).distinct()
        turma_choice = request.GET.get('valor')

        # Obtém os alunos da turma selecionada
        turma = Turma.objects.filter(numero=turma_choice).first()
        alunos = Aluno.objects.filter(turma=turma).values_list(
            'nome', flat=True).distinct()

        return render(request, 'cadastros_notas/cadastro_nota.html', {
            'avaliacoes': avaliacoes,
            'av_turmas': turmas_da_avaliacao,
            'form_action': reverse('avaliacao:cadastro_nota'),
            'alunos': alunos,
        })
    else:
        try:
            professor = Professor.objects.get(user=request.user)
        except:
            return HttpResponse('Usuário logado não está acossiado a um professor')

        # Coleta dados do formulário POST
        turma_numero = request.POST.get('turma_numero')
        av_choice = request.POST.get('valor')

        # Obtém a avaliação selecionada
        avaliacao = Avaliacao.objects.filter(
            turma_disciplina__avaliacao_turma_disciplina__titulo=av_choice,
            turma_disciplina__turma__numero=turma_numero).first()
        turma = Turma.objects.filter(numero=turma_numero).first()

        # Processa notas em lote
        # Os campos dinâmicos vêm do formulário como 'aluno_1', 'aluno_2', etc.
        # e 'nota_1', 'nota_2', etc.
        contador = 0
        alunos_processados = 0

        while True:
            contador += 1
            aluno_nome = request.POST.get(f'aluno_{contador}')

            # Para de processar quando não houver mais alunos
            if not aluno_nome:
                break

            # Obtém a pontuação do aluno
            nota = request.POST.get(f'nota_{contador}')

            try:
                # Localiza o aluno na turma
                aluno = Aluno.objects.filter(
                    nome=aluno_nome, turma=turma).first()

                # Cria registro de nota
                Nota.objects.create(
                    aluno=aluno,
                    avaliacao=avaliacao,
                    pontuacao=nota,
                )
                alunos_processados += 1

            except Aluno.DoesNotExist:
                messages.error(request, f'Aluno {aluno_nome} não encontrado')
                continue

        # Exibe mensagem de sucesso e redireciona
        messages.success(
            request, f'Registradas notas para {alunos_processados} alunos!')
        return redirect('avaliacao:cadastro_nota')
