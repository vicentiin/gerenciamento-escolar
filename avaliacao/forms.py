from django import forms 
from .models import (
    Avaliacao,
    Nota,
)

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['titulo', 'descricao', 'arquivo', 'status', 'turma_disciplina', 'data_aplicacao', 'periodo_letivo']
        widgets = {
            'data_aplicacao': forms.DateInput(attrs = {'class':'data', 'type': 'date'})
        }