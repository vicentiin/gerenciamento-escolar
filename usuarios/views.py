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
        data = {'form_action': reverse('usuarios:cadastro_admin')}
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
        data = {'form': form, 'form_action': reverse('usuarios:cadastro_professor')}
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
                user = User.objects.create_user(username = username, email = email, password = password)
                professor = form.save(commit = False)
                professor.user = user
                professor.save()

                professores_group = Group.objects.get(name = 'Professores')
                user.groups.add(professores_group)

                return HttpResponse('Professor Cadastrado com sucesso')





def cadastro_coordenador(request):
    if request.method == "GET":
        form = CoordenadorForm()
        data = {'form': form, 'form_action': reverse('usuarios:cadastro_coordenador')}
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
                user = User.objects.create_user(username = username, email = email, password = password)
                coordenador = form.save(commit = False)
                coordenador.user = user
                coordenador.save()
                
                coordenador_group = Group.objects.get(name = 'Coordenadores')
                user.groups.add(coordenador_group)

                return HttpResponse('Coordenador Cadastrado com sucesso')



def cadastro_aluno(request):
    if request.method == "GET":
        form = AlunoForm()
        data = {'form': form, 'form_action': reverse('usuarios:cadastro_aluno')}
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
                user = User.objects.create_user(username = username, email = email, password = password )
                aluno = form.save(commit = False)
                aluno.user = user
                aluno.save()

                alunos_group = Group.objects.get(name = 'Alunos')
                user.groups.add(alunos_group)

                return HttpResponse('Aluno Cadastrado com sucesso')


def login(request):
    if request.method == "GET":
        data = {'form_action': reverse('usuarios:login')}
        return render(request, 'login.html', data)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login_django(request, user)

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


@login_required(login_url= '/auth/login/')
def tela_admin(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse('Usuário não autenticado.')

        if not request.user.is_superuser:
            return HttpResponse('Acesso negado. Você não é administrador.')

        nome_admin = request.user.username
        admin_id = f'Matrícula: {request.user.id}'
        go_to_cadastro_aluno = reverse('usuarios:cadastro_aluno')
        go_to_cadastro_professor = reverse('usuarios:cadastro_professor')
        got_to_cadastro_coordenador = reverse('usuarios:cadastro_coordenador')
        cad_aluno = "Cadastrar aluno(a)"
        cad_professor = "Cadastrar professor(a)"
        cad_coordenador = "Cadastrar coordenador(a)"
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


@login_required(login_url= '/auth/login/')
def tela_professor(request):
    if request.method == "GET":
        try:
            professor = Professor.objects.get(user=request.user)
        except Professor.DoesNotExist:
            return HttpResponse('Usuário não associado a um professor')

        nome_prof = professor.nome
        prof_id = f'Matrícula: {professor.matricula}'
        go_to_cadastro_av = reverse('avaliacao:cadastro_avaliacao')
        go_to_cadastro_falta = reverse('turmas:cadastro_falta')
        got_to_cadastro_nota = reverse('avaliacao:cadastro_nota')
        cad_av = "Cadastrar Avaliação"
        cad_falta = "Registrar falta"
        cad_nota = "Inserir nota"
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


@login_required(login_url= '/auth/login/')
def tela_coordenador(request):
    if request.method == "GET":
        try:
            coordenador = Coordenador.objects.get(user=request.user)
        except Coordenador.DoesNotExist:
            return HttpResponse('Usuário não associado a um Coordenador')

        nome_coord = coordenador.nome
        coord_id = f'Matrícula: {coordenador.matricula}'
        go_to_cadastro_disciplina = reverse('turmas:cadastro_disciplina')
        go_to_cadastro_turma = reverse('turmas:cadastro_turma')
        cad_disciplina = "Cadastrar disciplina"
        cad_turma = "Cadastrar turma"
        data = {'nome': nome_coord,
                'matricula': coord_id,
                'cadastro_disciplina': go_to_cadastro_disciplina,
                'cadastro_turma': go_to_cadastro_turma,
                'funcao1': cad_disciplina,
                'funcao2': cad_turma,
                }
        return render(request, 'telas_users/coordenador.html', data)

