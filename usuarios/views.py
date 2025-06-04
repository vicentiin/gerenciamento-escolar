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
    if request.method == "GET":
        data = {'form_action': reverse('cadastro_admin')}
        return render(request, 'cadastros_users/cadastro_admin.html', data)
    else: 
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')

        user_cadastrado = User.objects.filter(username = username).first()
        if user_cadastrado:
            return HttpResponse('Super User já cadastrado!')

        user = User.objects.create_user(username = username, email = email, password = password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return HttpResponse('Super user cadastrado com sucesso!')
        


        
def cadastro_professor(request):
    if request.method == "GET":
        form = ProfessorForm()
        data = {'form': form, 'form_action': reverse('cadastro_professor')}
        return render(request, 'cadastros_users/cadastro_professor.html', data)
    else:
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')

        professor_cadastrado = Professor.objects.filter(cpf = cpf).first()
        if professor_cadastrado:
            return HttpResponse('Usuário já cadastrado!')
        else:
            form = ProfessorForm(request.POST or None)
            if form.is_valid():
                form.save()

                user = User.objects.create_user(username = username, email = email, password = password)
                professores_group = Group.objects.get(name = 'Professores')
                user.groups.add(professores_group)
                user.save()

                return HttpResponse('Professor Cadastrado com sucesso')





def cadastro_coordenador(request):
    if request.method == "GET":
        form = CoordenadorForm()
        data = {'form': form, 'form_action': reverse('cadastro_coordenador')}
        return render(request, 'cadastros_users/cadastro_coordenador.html', data)
    else:
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')

        aluno_cadastrado = Coordenador.objects.filter(cpf = cpf).first()
        if aluno_cadastrado:
            return HttpResponse(f"Usuário {username} cadastrado!")
        else:
            form = CoordenadorForm(request.POST or None)
            if form.is_valid():
                form.save()

                user = User.objects.create_user(username = username, email = email, password = password)
                alunos_group = Group.objects.get(name = 'Coordenadores')
                user.groups.add(alunos_group)
                user.save()

                return HttpResponse('Coordenador Cadastrado com sucesso')



def cadastro_aluno(request):
    if request.method == "GET":
        form = AlunoForm()
        data = {'form': form, 'form_action': reverse('cadastro_aluno')}
        return render(request, 'cadastros_users/cadastro_aluno.html', data)
    else:
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        birth = request.POST.get('data_nascimento')

        aluno_cadastrado = Coordenador.objects.filter(cpf = cpf).first()
        if aluno_cadastrado:
            return HttpResponse(f"Aluno {username} cadastrado!")
        else:
            form = AlunoForm(request.POST or None)
            if form.is_valid():
                form.save()

                user = User.objects.create_user(username = username, email = email, password = password )
                alunos_group = Group.objects.get(name = 'Alunos')
                user.groups.add(alunos_group)
                user.save()

                return HttpResponse('Aluno Cadastrado com sucesso')

@requires_csrf_token
def login(request):
    if request.method == "GET":
        data = {'form_action': reverse('login')}
        return render(request, 'login.html', data)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login_django(request, user)

            #Alterar para um redirect para a página de acordo com cada user
            return HttpResponse('autenticado')
        else:
            return HttpResponse('Senha ou usuário inválidos')

