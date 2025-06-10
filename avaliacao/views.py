from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote
from django.contrib import messages
from .forms import (
    AvaliacaoForm,
)
from usuarios.models import(
    Professor,
    Aluno,
)
from turmas.models import(
    Turma_Disciplina,
    Turma,
)
from .models import (
    Avaliacao,
    Nota,
)

# Create your views here.
def cadastro_avaliacao(request):
    if request.method == "GET":
        form = AvaliacaoForm()
        data = {'form': form, 'form_action': reverse('avaliacao:cadastro_avaliacao')}
        return render(request, 'cadastros_avaliacoes/cadastro_avaliacao.html', data)
    else:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        arquivo = request.FILES.get('arquivo')
        status = request.POST.get('status')
        turma_disciplina = request.POST.getlist('turma_disciplina')
        data_aplicacao = request.POST.get('data_aplicacao')
        periodo_letivo = request.POST.get('periodo_letivo')

        avaliacao_cadastrada = Avaliacao.objects.filter(periodo_letivo = periodo_letivo, data_aplicacao = data_aplicacao).first()
        if avaliacao_cadastrada:
            return HttpResponse('Avaliação nesse período já aplicada!')
        else:
            form = AvaliacaoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

            return HttpResponse('dados enviados')

@login_required(login_url= '/auth/login/')
def cadastro_nota(request):
    if request.method == "GET":
        try:
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
            turmas_da_avaliacao = Turma.objects.filter(
                turma_disciplina__avaliacao_turma_disciplina__titulo=av_choice,
                turma_disciplina__professor=professor
            ).distinct().values_list('numero', flat=True)

        # Verifica se é requisição AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'turmas': list(turmas_da_avaliacao),
                'avaliacao': av_choice
            })

        turmas = Turma_Disciplina.objects.filter(professor=professor).values_list('turma__numero', flat=True).distinct()
        turma_choice = request.GET.get('valor')

        turma = Turma.objects.filter(numero = turma_choice).first()
        alunos = Aluno.objects.filter(turma = turma).values_list('nome', flat=True).distinct()

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

        turma_numero = request.POST.get('turma_numero')
        av_choice = request.POST.get('valor')
        avaliacao = Avaliacao.objects.filter(
            turma_disciplina__avaliacao_turma_disciplina__titulo=av_choice,
            turma_disciplina__turma__numero=turma_numero).first()
        turma = Turma.objects.filter(numero = turma_numero).first()

        contador = 0
        alunos_processados = 0

        while True:
            contador += 1
            aluno_nome = request.POST.get(f'aluno_{contador}')

            if not aluno_nome:
                break

            nota = request.POST.get(f'nota_{contador}')

            try:
                aluno = Aluno.objects.filter(nome=aluno_nome, turma=turma).first()
    
                Nota.objects.create(
                    aluno = aluno,
                    avaliacao = avaliacao,
                    pontuacao = nota,
                )
                alunos_processados += 1

            except Aluno.DoesNotExist:
                messages.error(request, f'Aluno {aluno_nome} não encontrado')
                continue
        
        messages.success(request, f'Registradas notas para {alunos_processados} alunos!')
        return redirect('avaliacao:cadastro_nota')
