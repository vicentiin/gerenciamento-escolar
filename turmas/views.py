from django.shortcuts import render
from django.http import HttpResponse 
from django.urls import reverse
from .models import (
    Turma,
    Disciplina,
    Turma_Disciplina,
    Falta,
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
        data = {'form': form, 'form_action': reverse('cadastro_turma')}
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
        data = {'form': form, 'form_action': reverse('cadastro_turmaDisciplina')}
        return render(request, 'cadastros_turmas/cadastro_turmaDisciplina.html', data)
    else:
        turma = request.POST.get('turma')
        disciplina = request.POST.get('disciplina')

        turma_disciplina_cadastrada = Turma_Disciplina.objects.filter(turma = turma, disciplina = disciplina).first()
        if turma_disciplina_cadastrada:
            return HttpResponse('Essa turma e disciplina já estão vinculadas')
        else:
            form = Turma_DisciplinaForm(request.POST or None)
            if form.is_valid():
                form.save()

            return HttpResponse('Turma_disciplina cadastradas')


def cadastro_disciplina(request):
    if request.method == "GET":
        form = DisciplinaForm()
        data = {'form': form, 'form_action': reverse('cadastro_disciplina')}
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


#def cadastro_falta(request):
