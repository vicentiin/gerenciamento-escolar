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
from usuarios.models import(
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
    if request.method == "GET":
        form = TurmaForm()
        data = {'form': form, 'form_action': reverse('turmas:cadastro_turma')}
        return render(request, 'cadastros_turmas/cadastro_turma.html', data)
    else:
        numero = request.POST.get('numero')
        sala = request.POST.get('sala')
        quantidade_maxima = request.POST.get('quantidade_maxima')

        turma_cadastrada_n = Turma.objects.filter(numero = numero).first()
        turma_cadastrada_s = Turma.objects.filter(sala = sala).first()
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
    if request.method == "GET":
        form = Turma_DisciplinaForm()
        data = {'form': form, 'form_action': reverse('turmas:cadastro_turmaDisciplina')}
        return render(request, 'cadastros_turmas/cadastro_turmaDisciplina.html', data)
    else:
        turma = request.POST.get('turma')
        disciplina = request.POST.get('disciplina')
        professor = request.POST.get('professor')

        turma_disciplina_cadastrada = Turma_Disciplina.objects.filter(turma = turma, disciplina = disciplina).first()
        turma_disciplina_prof = Turma_Disciplina.objects.filter(turma = turma, disciplina = disciplina, professor = professor).first()
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
    if request.method == "GET":
        form = DisciplinaForm()
        data = {'form': form, 'form_action': reverse('turmas:cadastro_disciplina')}
        return render(request, 'cadastros_turmas/cadastro_disciplina.html', data)
    else:
        nome = request.POST.get('nome')

        disciplina_cadastrada = Disciplina.objects.filter(nome = nome).first()
        if disciplina_cadastrada:
            return HttpResponse('Essa Disciplina já foi cadastrada!')
        else:
            form = DisciplinaForm(request.POST or None)
            if form.is_valid():
                form.save()

            return HttpResponse('Dados enviados')

@login_required(login_url = '/auth/login/')
def cadastro_falta(request):    
    if request.method == "GET":
        try:
            professor = Professor.objects.get(user=request.user)
        except:
            return HttpResponse('Usuário logado não está acossiado a um professor')

        turmas = Turma_Disciplina.objects.filter(professor=professor).values_list('turma__numero', flat=True).distinct()
        turma_choice = request.GET.get('valor')

        turma = Turma.objects.filter(numero = turma_choice).first()
        alunos = Aluno.objects.filter(turma = turma).values_list('nome', flat=True).distinct()

        data = {'form_action': reverse('turmas:cadastro_falta'), 
                'turmas': turmas,   
                'alunos': alunos
                }
        return render(request, 'base_falta_turma.html', data)
    else:
        try:
            professor = Professor.objects.get(user=request.user)
        except:
            return HttpResponse('Usuário logado não está acossiado a um professor')

        turma_numero = request.POST.get('turma_numero')
        turma = Turma.objects.filter(numero = turma_numero).first()
        turma_disciplina = Turma_Disciplina.objects.filter(turma=turma, professor=professor).first()

        contador = 0
        alunos_processados = 0

        while True:
            contador += 1
            aluno_nome = request.POST.get(f'aluno_{contador}')

            if not aluno_nome:
                break

            falta_status = request.POST.get(f'falta_{contador}') == 'falta'

            try:
                aluno = Aluno.objects.filter(nome=aluno_nome, turma=turma).first()

                Falta.objects.create(
                    aluno = aluno,
                    turma_disciplina = turma_disciplina,
                    status = falta_status,
                    data = date.today()
                )
                alunos_processados += 1

            except Aluno.DoesNotExist:
                messages.error(request, f'Aluno {aluno_nome} não encontrado')
                continue

        messages.success(request, f'Registradas faltas para {alunos_processados} alunos!')
        return redirect('turmas:cadastro_falta')
    





