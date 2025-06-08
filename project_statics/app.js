function enviarTurma(button) {
    const valor = button.value;
    document.getElementById('turma_numero').value = valor;
    const url = `/auth-turmas/cadastro-falta/?valor=${valor}`;
    
    fetch(url)
        .then(response => response.text())
        .then(html => {
            // Cria um parser para extrair o conteúdo dos alunos
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Extrai todo o conteúdo do container de alunos
            const novosAlunos = doc.getElementById('alunos-container').innerHTML;
            
            // Atualiza o container de alunos na página atual
            document.getElementById('alunos-container').innerHTML = novosAlunos;
        })
        .catch(error => console.error('Error:', error));
}