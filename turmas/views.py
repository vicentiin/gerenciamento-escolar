"""
Módulo de Views para Gerenciamento de Turmas, Disciplinas e Faltas.

Este módulo contém as vistas para:
- Cadastro de turmas
- Vinculação de disciplinas a turmas e professores
- Cadastro de disciplinas
- Registro de faltas de alunos

Tipos de operações:
- GET: Exibição de formulários
- POST: Processamento e persistência de dados
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages
from .models import (
    Turma,
    Disciplina,
    Turma_Disciplina,
    Falta,
)
from usuarios.models import (
    Professor,
    Aluno,
)
from .forms import (
    TurmaForm,
    Turma_DisciplinaForm,
    DisciplinaForm

)

# Create your views here.


def cadastro_turma(request):
    """
    Realiza o cadastro de novas turmas.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de turma
    - POST: Processa o cadastro validando número e sala únicos

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Número da turma deve ser único
    - Sala deve estar disponível (não pode estar ocupada por outra turma)
    """
    if request.method == "GET":
        form = TurmaForm()
        data = {'form': form, 'form_action': reverse('turmas:cadastro_turma')}
        return render(request, 'cadastros_turmas/cadastro_turma.html', data)
    else:
        # Coleta dados do formulário
        numero = request.POST.get('numero')
        sala = request.POST.get('sala')
        quantidade_maxima = request.POST.get('quantidade_maxima')

        # Verifica se turma com esse número já existe
        turma_cadastrada_n = Turma.objects.filter(numero=numero).first()
        turma_cadastrada_s = Turma.objects.filter(sala=sala).first()
        if turma_cadastrada_n:
            return HttpResponse('Turma já cadastrada')
        elif turma_cadastrada_s:
            return HttpResponse(f'Sala já ocupada pela turma {turma_cadastrada_s.numero}')
        else:
            form = TurmaForm(request.POST or None)
            if form.is_valid():
                form.save()

            return HttpResponse('Dados enviados')


def cadastro_turmaDisciplina(request):
    """
    Realiza a vinculação de disciplinas a turmas e aloca professores.

    Metodos HTTP:
    - GET: Exibe o formulário de vinculação turma-disciplina
    - POST: Processa a vinculação validando duplicatas

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - A combinação turma+disciplina não pode ser duplicada
    - Um professor não pode ser alocado duas vezes na mesma turma e disciplina
    """
    if request.method == "GET":
        form = Turma_DisciplinaForm()
        data = {'form': form, 'form_action': reverse(
            'turmas:cadastro_turmaDisciplina')}
        return render(request, 'cadastros_turmas/cadastro_turmaDisciplina.html', data)
    else:
        # Coleta dados do formulário
        turma = request.POST.get('turma')
        disciplina = request.POST.get('disciplina')
        professor = request.POST.get('professor')

        # Verifica se a combinação turma+disciplina já existe
        turma_disciplina_cadastrada = Turma_Disciplina.objects.filter(
            turma=turma, disciplina=disciplina).first()
        turma_disciplina_prof = Turma_Disciplina.objects.filter(
            turma=turma, disciplina=disciplina, professor=professor).first()
        if turma_disciplina_cadastrada:
            return HttpResponse('Essa turma e disciplina já estão vinculadas')
        elif turma_disciplina_prof:
            return HttpResponse('Esse Professor já está alocado nessa turma')
        else:
            form = Turma_DisciplinaForm(request.POST or None)
            if form.is_valid():
                form.save()

            return HttpResponse('Turma_disciplina cadastradas')


def cadastro_disciplina(request):
    """
    Realiza o cadastro de novas disciplinas.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de disciplina
    - POST: Processa o cadastro validando duplicatas

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Nome da disciplina deve ser único
    """
    if request.method == "GET":
        form = DisciplinaForm()
        data = {'form': form, 'form_action': reverse(
            'turmas:cadastro_disciplina')}
        return render(request, 'cadastros_turmas/cadastro_disciplina.html', data)
    else:
        # Coleta dados do formulário
        nome = request.POST.get('nome')

        # Verifica se disciplina com esse nome já existe
        disciplina_cadastrada = Disciplina.objects.filter(nome=nome).first()
        if disciplina_cadastrada:
            return HttpResponse('Essa Disciplina já foi cadastrada!')
        else:
            form = DisciplinaForm(request.POST or None)
            if form.is_valid():
                form.save()

            return HttpResponse('Dados enviados')


@login_required(login_url='/auth/login/')
def cadastro_falta(request):
    """
    Realiza o registro de faltas de alunos por disciplina em uma turma.

    Metodos HTTP:
    - GET: Exibe formulário com seleção de turma e lista de alunos
    - POST: Processa o registro de faltas para múltiplos alunos

    Args:
        request (HttpRequest): Objeto de requisição HTTP contendo:
        - GET: 'valor' (parâmetro de query para número da turma)
        - POST: 'turma_numero' e campos dinâmicos 'aluno_X' e 'falta_X'

    Returns:
        HttpResponse: Página HTML com formulário (GET) ou redirecionamento com mensagem (POST)

    Fluxo:
    1. GET: Recupera turmas onde o professor está alocado
    2. Filtra alunos da turma selecionada
    3. POST: Processa registro de faltas em lote
    4. Cria registros Falta para cada aluno com status e data

    Requer autenticação e usuário associado a um Professor
    """
    if request.method == "GET":
        try:
            # Obtém o professor associado ao usuário logado
            professor = Professor.objects.get(user=request.user)
        except:
            return HttpResponse('Usuário logado não está acossiado a um professor')

        # Recupera as turmas em que o professor leciona
        turmas = Turma_Disciplina.objects.filter(professor=professor).values_list(
            'turma__numero', flat=True).distinct()
        turma_choice = request.GET.get('valor')

        # Obtém os alunos da turma selecionada
        turma = Turma.objects.filter(numero=turma_choice).first()
        alunos = Aluno.objects.filter(turma=turma).values_list(
            'nome', flat=True).distinct()

        data = {'form_action': reverse('turmas:cadastro_falta'),
                'turmas': turmas,
                'alunos': alunos
                }
        return render(request, 'cadastros_faltas/cadastro_falta.html', data)
    else:
        try:
            professor = Professor.objects.get(user=request.user)
        except:
            return HttpResponse('Usuário logado não está acossiado a um professor')

        # Coleta dados do formulário POST
        turma_numero = request.POST.get('turma_numero')
        turma = Turma.objects.filter(numero=turma_numero).first()
        turma_disciplina = Turma_Disciplina.objects.filter(
            turma=turma, professor=professor).first()

        # Processa faltas em lote
        # Os campos dinâmicos vêm do formulário como 'aluno_1', 'aluno_2', etc.
        # e 'falta_1', 'falta_2', etc. com valores 'falta' ou 'presente'
        contador = 0
        alunos_processados = 0

        while True:
            contador += 1
            aluno_nome = request.POST.get(f'aluno_{contador}')

            # Para de processar quando não houver mais alunos
            if not aluno_nome:
                break

            # Obtém o status de falta (True se marcado como 'falta')
            falta_status = request.POST.get(f'falta_{contador}') == 'falta'

            try:
                # Localiza o aluno na turma
                aluno = Aluno.objects.filter(
                    nome=aluno_nome, turma=turma).first()

                # Cria registro de falta com data atual
                Falta.objects.create(
                    aluno=aluno,
                    turma_disciplina=turma_disciplina,
                    status=falta_status,
                    data=date.today()
                )
                alunos_processados += 1

            except Aluno.DoesNotExist:
                messages.error(request, f'Aluno {aluno_nome} não encontrado')
                continue

        # Exibe mensagem de sucesso e redireciona
        messages.success(
            request, f'Registradas faltas para {alunos_processados} alunos!')
        return redirect('turmas:cadastro_falta')
