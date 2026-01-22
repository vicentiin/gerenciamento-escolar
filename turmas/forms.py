"""
Formulários para criação e edição de turmas, disciplinas e suas vinculações.

Este arquivo define formulários ModelForm para as entidades principais
do aplicativo de turmas.
"""

from django import forms
from .models import (
    Turma,
    Disciplina,
    Turma_Disciplina,
    Falta,
)


class TurmaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de turmas.

    Campos: número, sala, quantidade máxima de alunos
    """
    class Meta:
        model = Turma
        fields = ['numero', 'sala', 'quantidade_maxima']


class DisciplinaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de disciplinas.

    Campos: nome da disciplina
    """
    class Meta:
        model = Disciplina
        fields = ['nome']


class Turma_DisciplinaForm(forms.ModelForm):
    """
    Formulário para vinculação de disciplinas a turmas e alocação de professores.

    Campos: turma, disciplina, professor
    """
    class Meta:
        model = Turma_Disciplina
        fields = ['turma', 'disciplina', 'professor']
