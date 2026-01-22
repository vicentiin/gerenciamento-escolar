# Pontes para o Futuro - Sistema de Gestão Escolar

**Versão:** 1.0

> Sistema completo de gestão escolar online para administração de turmas, disciplinas, avaliações e registro de faltas.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Funcionalidades](#funcionalidades)
- [Funcionalidades Futuras - Versão 1.1](#funcionalidades-futuras)
- [Contribuindo](#contribuindo)
- [Contato](#contato)

---

## Sobre o Projeto

**Pontes para o Futuro** é um sistema de gestão escolar desenvolvido para apoiar a administração acadêmica de uma escola online. A aplicação permite o gerenciamento de usuários (alunos, professores, coordenadores e administradores), turmas, disciplinas, avaliações e registro de faltas, oferecendo uma base sólida para o controle das operações educacionais.

O projeto foi desenvolvido com foco em backend e aplicações web, utilizando Python e Django, com o objetivo de consolidar meus conhecimentos em desenvolvimento web, modelagem de dados e regras de negócio em um sistema real.

### Objetivos

- Centralizar informações acadêmicas
- Facilitar a gestão de turmas e disciplinas
- Permitir registro eletrônico de avaliações e notas
- Controlar frequência de alunos
- Fornecer diferentes níveis de acesso por tipo de usuário

---

## Tecnologias Utilizadas

- **Backend:** Python 3.x com Django 5.1
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (recomendado para produção)
- **Frontend:** HTML5, CSS3, JavaScript
- **Servidor:** Gunicorn
- **Dependências principais:**
  - Django 5.1.7
  - Gunicorn 23.0.0
  - ASGI (asgiref 3.8.1)
  - SQLparse 0.5.3
  - WhiteNoise 6.9.0

---

## Instalação

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### Passos de Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/pontes-para-o-futuro.git
   cd projeto-escola/pontesParaoFuturo
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

6. **Crie um usuário administrador:**
   ```bash
   python manage.py createsuperuser
   ```

---

## Uso

### Iniciar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`

### Acessar a Aplicação

- **Página Inicial:** http://localhost:8000
- **Painel Admin:** http://localhost:8000/admin (com credenciais de superuser)
- **Login:** http://localhost:8000/auth/login

### Fluxo de Uso

1. **Administrador** cria usuários (alunos, professores, coordenadores)
2. **Coordenadores** gerenciam turmas e disciplinas
3. **Professores** registram avaliações e notas
4. **Professores** registram faltas de alunos
5. **Alunos** consultam seus dados acadêmicos

---

## Funcionalidades

### 👤 Gerenciamento de Usuários

- Cadastro de diferentes tipos de usuários (Admin, Professor, Coordenador, Aluno)
- Autenticação segura com Django Auth
- Controle de acesso por tipo de usuário
- Perfis com informações pessoais (CPF, data de nascimento, matrícula)

### 📚 Gerenciamento de Turmas e Disciplinas

- Criação e gerenciamento de turmas
- Cadastro de disciplinas
- Vinculação de disciplinas a turmas
- Alocação de professores por disciplina

### 📝 Avaliações e Notas

- Cadastro de avaliações com arquivos anexados
- Aplicação de avaliações a múltiplas turmas
- Registro de notas de alunos
- Classificação de relevância de notas
- Rastreamento de período letivo

### 📋 Registro de Faltas

- Registro de faltas por disciplina
- Controle de presença/ausência
- Rastreamento por data
- Relatórios de frequência

### 🔐 Segurança

- Autenticação obrigatória para acesso
- Controle de permissões por tipo de usuário
- Proteção CSRF em formulários
- Dados sensíveis (senhas, CPF) protegidos

---

## Funcionalidades Futuras
Uma **versão futura** do Pontes para o Futuro está planejada para evoluir para uma arquitetura baseada em **API REST**, permitindo que o sistema seja consumido por diferentes interfaces, como aplicações web modernas, aplicativos mobile ou integrações externas.

---

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork o projeto**
2. **Crie uma branch para sua feature:**
   ```bash
   git checkout -b feature/SuaFeature
   ```
3. **Commit suas mudanças:**
   ```bash
   git commit -m 'Add some SuaFeature'
   ```
4. **Push para a branch:**
   ```bash
   git push origin feature/SuaFeature
   ```
5. **Abra um Pull Request**

### Diretrizes de Contribuição

- Mantenha o código bem documentado
- Siga as convenções de estilo do projeto
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário

---

## Contato

Para dúvidas, sugestões ou relatos de bugs:

<a href="mailto:vicentemirandaoffice@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
</a>

<a href="https://www.linkedin.com/in/carlosfilipevicentemiranda/">
    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

Caso o mailto não responda: 
<a href="https://mail.google.com/mail/?view=cm&fs=1&to=vicentemirandaoffice@gmail.com">
    Enviar email
</a>

---

**Desenvolvido com ❤️ e responsabilidade**
