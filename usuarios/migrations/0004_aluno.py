# Generated by Django 5.1.7 on 2025-04-30 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_rename_updated_at_alunos_update_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('nome', models.CharField(max_length=70, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('data_nascimento', models.DateField(verbose_name='Data de nascimento')),
                ('status', models.BooleanField(default=True, verbose_name='Ativo')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('matricula', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
                'ordering': ['nome'],
            },
        ),
    ]
