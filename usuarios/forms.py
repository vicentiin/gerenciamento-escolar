"""
Formulários para criação e edição de usuários do sistema.

Este arquivo define formulários ModelForm baseados nos modelos de usuários
(Aluno, Coordenador e Professor) para renderização em templates HTML.
"""

from django import forms  # type:ignore
from .models import (
    Aluno,
    Coordenador,
    Professor,
)


class AlunoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de alunos.

    Campos: nome, cpf, data_nascimento, senha
    Customização: Campo de data com input type='date' para melhor UX
    """
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'data_nascimento', 'senha']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'birth', 'type': 'date'})
        }


class CoordenadorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de coordenadores.

    Campos: nome, cpf, data_nascimento, segmento, email, senha
    Customização: Campo de data com input type='date' para melhor UX
    """
    class Meta:
        model = Coordenador
        fields = ['nome', 'cpf', 'data_nascimento',
                  'segmento', 'email', 'senha']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'birth', 'type': 'date'})
        }


class ProfessorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de professores.

    Campos: nome, cpf, data_nascimento, segmento, email, senha
    Customização: Campo de data com input type='date' para melhor UX
    """
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'data_nascimento',
                  'segmento', 'email', 'senha']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'birth', 'type': 'date'})
        }
