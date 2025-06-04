from django import forms #type:ignore
from .models import (
    Aluno,
    Coordenador,
    Professor,
)

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'data_nascimento', 'senha']
        widgets = {
            'data_nascimento': forms.DateInput(attrs = {'class':'birth', 'type': 'date'})
        }


class CoordenadorForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = ['nome', 'cpf', 'data_nascimento', 'segmento', 'email', 'senha']
        widgets = {
            'data_nascimento': forms.DateInput(attrs = {'class':'birth', 'type': 'date'})
        }


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'cpf', 'data_nascimento', 'segmento', 'email', 'senha']
        widgets = {
            'data_nascimento': forms.DateInput(attrs = {'class':'birth', 'type': 'date'})
        }
