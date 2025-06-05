from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .forms import (
    AvaliacaoForm,
)
from .models import (
    Avaliacao,
)

# Create your views here.
def cadastro_avaliacao(request):
    if request.method == "GET":
        form = AvaliacaoForm()
        data = {'form': form, 'form_action': reverse('cadastro_avaliacao')}
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


