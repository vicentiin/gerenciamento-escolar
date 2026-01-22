"""
Módulo de Views para Gerenciamento de Usuários (Usuarios).

Este módulo contém as vistas para autenticação e gerenciamento de usuários
do sistema de gestão escolar. Inclui funções para:
- Cadastro de diferentes tipos de usuários (Admin, Professor, Coordenador, Aluno)
- Autenticação e login de usuários
- Exibição de telas personalizadas conforme o tipo de usuário

Tipos de usuários suportados:
- Admin (Super User): Acesso total ao sistema
- Professor: Gestão de avaliações, notas e faltas
- Coordenador: Gestão de disciplinas e turmas
- Aluno: Consulta de dados acadêmicos
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as login_django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from .models import (
    Professor,
    Coordenador,
    Aluno
)
from .forms import (
    AlunoForm,
    ProfessorForm,
    CoordenadorForm,
)


def cadastro_admin(request):
    """
    Realiza o cadastro de um novo administrador (Super User) do sistema.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de admin
    - POST: Processa o cadastro de um novo super usuário

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Verifica se o usuário já existe no banco de dados
    - Criação de usuário com permissões de staff e superusuário
    """
    if request.method == "GET":
        data = {'form_action': reverse('usuarios:cadastro_admin')}
        return render(request, 'cadastros_users/cadastro_admin.html', data)
    else:
        # Coleta dados do formulário
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')

        # Verifica se o usuário já foi cadastrado
        user_cadastrado = User.objects.filter(username=username).first()
        if user_cadastrado:
            return HttpResponse('Super User já cadastrado!')

        # Cria novo usuário com permissões de administrador
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return HttpResponse('Super user cadastrado com sucesso!')


def cadastro_professor(request):
    """
    Realiza o cadastro de um novo professor no sistema.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de professor
    - POST: Processa o cadastro de um novo professor

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Verifica se o CPF já foi cadastrado
    - Valida dados do formulário com ProfessorForm
    - Associa novo usuário ao grupo 'Professores'

    Processo:
    1. Cria um novo usuário Django
    2. Cria registro de professor vinculado ao usuário
    3. Adiciona usuário ao grupo de Professores
    """
    if request.method == "GET":
        form = ProfessorForm()
        data = {'form': form, 'form_action': reverse(
            'usuarios:cadastro_professor')}
        return render(request, 'cadastros_users/cadastro_professor.html', data)
    else:
        # Coleta dados do formulário
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')

        # Verifica se professor com esse CPF já existe
        professor_cadastrado = Professor.objects.filter(cpf=cpf).first()
        if professor_cadastrado:
            return HttpResponse('Usuário já cadastrado!')
        else:
            form = ProfessorForm(request.POST or None)
            if form.is_valid():
                # Cria novo usuário Django
                user = User.objects.create_user(
                    username=username, email=email, password=password)

                # Cria registro de professor
                professor = form.save(commit=False)
                professor.user = user
                professor.save()

                # Adiciona usuário ao grupo de Professores
                professores_group = Group.objects.get(name='Professores')
                user.groups.add(professores_group)

                return HttpResponse('Professor Cadastrado com sucesso')


def cadastro_coordenador(request):
    """
    Realiza o cadastro de um novo coordenador no sistema.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de coordenador
    - POST: Processa o cadastro de um novo coordenador

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Verifica se o CPF já foi cadastrado
    - Valida dados do formulário com CoordenadorForm
    - Associa novo usuário ao grupo 'Coordenadores'

    Processo:
    1. Cria um novo usuário Django
    2. Cria registro de coordenador vinculado ao usuário
    3. Adiciona usuário ao grupo de Coordenadores
    """
    if request.method == "GET":
        form = CoordenadorForm()
        data = {'form': form, 'form_action': reverse(
            'usuarios:cadastro_coordenador')}
        return render(request, 'cadastros_users/cadastro_coordenador.html', data)
    else:
        # Coleta dados do formulário
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')

        # Verifica se coordenador com esse CPF já existe
        aluno_cadastrado = Coordenador.objects.filter(cpf=cpf).first()
        if aluno_cadastrado:
            return HttpResponse(f"Usuário {username} cadastrado!")
        else:
            form = CoordenadorForm(request.POST or None)
            if form.is_valid():
                # Cria novo usuário Django
                user = User.objects.create_user(
                    username=username, email=email, password=password)

                # Cria registro de coordenador
                coordenador = form.save(commit=False)
                coordenador.user = user
                coordenador.save()

                # Adiciona usuário ao grupo de Coordenadores
                coordenador_group = Group.objects.get(name='Coordenadores')
                user.groups.add(coordenador_group)

                return HttpResponse('Coordenador Cadastrado com sucesso')


def cadastro_aluno(request):
    """
    Realiza o cadastro de um novo aluno no sistema.

    Metodos HTTP:
    - GET: Exibe o formulário de cadastro de aluno
    - POST: Processa o cadastro de um novo aluno

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário (GET) ou mensagem de sucesso/erro (POST)

    Validações:
    - Verifica se o CPF já foi cadastrado
    - Valida dados do formulário com AlunoForm
    - Associa novo usuário ao grupo 'Alunos'

    Processo:
    1. Cria um novo usuário Django
    2. Cria registro de aluno vinculado ao usuário
    3. Adiciona usuário ao grupo de Alunos
    """
    if request.method == "GET":
        form = AlunoForm()
        data = {'form': form, 'form_action': reverse(
            'usuarios:cadastro_aluno')}
        return render(request, 'cadastros_users/cadastro_aluno.html', data)
    else:
        # Coleta dados do formulário
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        birth = request.POST.get('data_nascimento')

        # Verifica se aluno com esse CPF já existe
        aluno_cadastrado = Coordenador.objects.filter(cpf=cpf).first()
        if aluno_cadastrado:
            return HttpResponse(f"Aluno {username} cadastrado!")
        else:
            form = AlunoForm(request.POST or None)
            if form.is_valid():
                # Cria novo usuário Django
                user = User.objects.create_user(
                    username=username, email=email, password=password)

                # Cria registro de aluno
                aluno = form.save(commit=False)
                aluno.user = user
                aluno.save()

                # Adiciona usuário ao grupo de Alunos
                alunos_group = Group.objects.get(name='Alunos')
                user.groups.add(alunos_group)

                return HttpResponse('Aluno Cadastrado com sucesso')


def login(request):
    """
    Realiza a autenticação e login de usuários no sistema.

    Metodos HTTP:
    - GET: Exibe o formulário de login
    - POST: Processa a autenticação e faz login do usuário

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML do formulário de login (GET) ou redirecionamento 
                     conforme o tipo de usuário (POST)

    Fluxo de redirecionamento:
    - Professor: Redireciona para tela_professor
    - Coordenador: Redireciona para tela_coordenador
    - Admin (Super User): Redireciona para tela_admin
    - Sem grupo: Retorna mensagem de erro

    Validações:
    - Verifica se usuário e senha são válidos
    - Verifica o grupo/tipo do usuário para redirecionamento
    """
    if request.method == "GET":
        data = {'form_action': reverse('usuarios:login')}
        return render(request, 'login.html', data)
    else:
        # Coleta dados de login
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário
        user = authenticate(username=username, password=password)

        if user:
            # Faz login do usuário
            login_django(request, user)

            # Redireciona conforme o tipo de usuário
            if Professor.objects.filter(user=request.user).exists():
                return redirect('usuarios:tela_professor')

            elif Coordenador.objects.filter(user=request.user).exists():
                return redirect('usuarios:tela_coordenador')

            elif request.user.is_superuser:
                return redirect('usuarios:tela_admin')

            else:
                return HttpResponse('Usuário não autenticado!')
        else:
            return HttpResponse('Senha ou usuário inválidos')


@login_required(login_url='/auth/login/')
def tela_admin(request):
    """
    Exibe a tela principal do administrador do sistema.

    Metodos HTTP:
    - GET: Exibe o painel de administrador com opções de cadastro

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML com o painel de administrador

    Validações de acesso:
    - Requer autenticação (decorator @login_required)
    - Verifica se o usuário é super usuário

    Funcionalidades disponíveis:
    - Cadastro de alunos
    - Cadastro de professores
    - Cadastro de coordenadores

    Contexto renderizado:
    - nome: Nome do admin (username)
    - matricula: ID do admin formatado como matrícula
    - Links para cadastros e rótulos das funções
    """
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse('Usuário não autenticado.')

        if not request.user.is_superuser:
            return HttpResponse('Acesso negado. Você não é administrador.')

        # Prepara dados do admin
        nome_admin = request.user.username
        admin_id = f'Matrícula: {request.user.id}'

        # Gera URLs para páginas de cadastro
        go_to_cadastro_aluno = reverse('usuarios:cadastro_aluno')
        go_to_cadastro_professor = reverse('usuarios:cadastro_professor')
        got_to_cadastro_coordenador = reverse('usuarios:cadastro_coordenador')

        # Rótulos das funções disponíveis
        cad_aluno = "Cadastrar aluno(a)"
        cad_professor = "Cadastrar professor(a)"
        cad_coordenador = "Cadastrar coordenador(a)"

        # Monta dicionário de contexto
        data = {'nome': nome_admin,
                'matricula': admin_id,
                'cadastro_aluno': go_to_cadastro_aluno,
                'cadastro_professor': go_to_cadastro_professor,
                'cadastro_coordenador': got_to_cadastro_coordenador,
                'funcao1': cad_aluno,
                'funcao2': cad_professor,
                'funcao3': cad_coordenador
                }
        return render(request, 'telas_users/admin.html', data)


@login_required(login_url='/auth/login/')
def tela_professor(request):
    """
    Exibe a tela principal do professor no sistema.

    Metodos HTTP:
    - GET: Exibe o painel do professor com suas funcionalidades

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML com o painel do professor ou mensagem de erro

    Validações de acesso:
    - Requer autenticação (decorator @login_required)
    - Verifica se o usuário está associado a um registro de Professor

    Funcionalidades disponíveis:
    - Cadastro de Avaliações
    - Registrar faltas de alunos
    - Inserir notas

    Contexto renderizado:
    - nome: Nome do professor
    - matricula: Número de matrícula do professor
    - Links para as funcionalidades
    - Rótulos descritivos das funções
    """
    if request.method == "GET":
        try:
            # Obtém o registro do professor associado ao usuário
            professor = Professor.objects.get(user=request.user)
        except Professor.DoesNotExist:
            return HttpResponse('Usuário não associado a um professor')

        # Prepara dados do professor
        nome_prof = professor.nome
        prof_id = f'Matrícula: {professor.matricula}'

        # Gera URLs para funcionalidades
        go_to_cadastro_av = reverse('avaliacao:cadastro_avaliacao')
        go_to_cadastro_falta = reverse('turmas:cadastro_falta')
        got_to_cadastro_nota = reverse('avaliacao:cadastro_nota')

        # Rótulos das funções disponíveis
        cad_av = "Cadastrar Avaliação"
        cad_falta = "Registrar falta"
        cad_nota = "Inserir nota"

        # Monta dicionário de contexto
        data = {'nome': nome_prof,
                'matricula': prof_id,
                'cadastro_av': go_to_cadastro_av,
                'cadastro_falta': go_to_cadastro_falta,
                'cadastro_nota': got_to_cadastro_nota,
                'funcao1': cad_av,
                'funcao2': cad_falta,
                'funcao3': cad_nota
                }
        return render(request, 'telas_users/professor.html', data)


@login_required(login_url='/auth/login/')
def tela_coordenador(request):
    """
    Exibe a tela principal do coordenador no sistema.

    Metodos HTTP:
    - GET: Exibe o painel do coordenador com suas funcionalidades

    Args:
        request (HttpRequest): Objeto de requisição HTTP

    Returns:
        HttpResponse: Página HTML com o painel do coordenador ou mensagem de erro

    Validações de acesso:
    - Requer autenticação (decorator @login_required)
    - Verifica se o usuário está associado a um registro de Coordenador

    Funcionalidades disponíveis:
    - Cadastro de disciplinas
    - Cadastro de turmas

    Contexto renderizado:
    - nome: Nome do coordenador
    - matricula: Número de matrícula do coordenador
    - Links para as funcionalidades
    - Rótulos descritivos das funções
    """
    if request.method == "GET":
        try:
            # Obtém o registro do coordenador associado ao usuário
            coordenador = Coordenador.objects.get(user=request.user)
        except Coordenador.DoesNotExist:
            return HttpResponse('Usuário não associado a um Coordenador')

        # Prepara dados do coordenador
        nome_coord = coordenador.nome
        coord_id = f'Matrícula: {coordenador.matricula}'

        # Gera URLs para funcionalidades
        go_to_cadastro_disciplina = reverse('turmas:cadastro_disciplina')
        go_to_cadastro_turma = reverse('turmas:cadastro_turma')

        # Rótulos das funções disponíveis
        cad_disciplina = "Cadastrar disciplina"
        cad_turma = "Cadastrar turma"

        # Monta dicionário de contexto
        data = {'nome': nome_coord,
                'matricula': coord_id,
                'cadastro_disciplina': go_to_cadastro_disciplina,
                'cadastro_turma': go_to_cadastro_turma,
                'funcao1': cad_disciplina,
                'funcao2': cad_turma,
                }
        return render(request, 'telas_users/coordenador.html', data)