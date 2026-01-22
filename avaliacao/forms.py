"""
Formulários para criação e edição de avaliações.

Este arquivo define formulários ModelForm para as entidades de avaliação.
"""

from django import forms
from .models import (
    Avaliacao,
    Nota,
)


class AvaliacaoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de avaliações.

    Campos: título, descrição, arquivo, status, turmas-disciplinas, 
    data de aplicação, período letivo

    Customização: Campo de data com input type='date' para melhor UX
    """
    class Meta:
        model = Avaliacao
        fields = ['titulo', 'descricao', 'arquivo', 'status',
                  'turma_disciplina', 'data_aplicacao', 'periodo_letivo']
        widgets = {
            'data_aplicacao': forms.DateInput(attrs={'class': 'data', 'type': 'date'})
        }
