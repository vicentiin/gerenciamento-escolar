from django import forms
from .models import (
    Turma,
    Disciplina,
    Turma_Disciplina,
    Falta,
)

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['numero', 'sala', 'quantidade_maxima']

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome']

class Turma_DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Turma_Disciplina
        fields = ['turma', 'disciplina', 'professor']
