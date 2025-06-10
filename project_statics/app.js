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


function enviarTurmaNota(button) {
    const valor = button.value;
    document.getElementById('turma_numero').value = valor;
    const url = `/auth-avaliacao/cadastro-nota/?valor=${valor}`;
    
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


function enviarAv(button) {
    const valor = encodeURIComponent(button.value);
    
    fetch(`/auth-avaliacao/cadastro-nota/?valor=${valor}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro na requisição');
        return response.json();
    })
    .then(data => {
        // Atualiza a lista de turmas
        const turmasContainer = document.getElementById('turmas-container');
        turmasContainer.innerHTML = '';
        
        if (data.turmas && data.turmas.length > 0) {
            data.turmas.forEach(turma => {
                const divContainer = document.createElement('div');
                divContainer.className = 'btn-curmas';
                
                // Cria o botão
                const botao = document.createElement('button');
                botao.className = 'btn-turma';
                botao.value = turma;
                botao.textContent = turma;
                botao.onclick = function() { enviarTurmaNota(this); };
                
                // Adiciona o botão à div container
                divContainer.appendChild(botao);
                
                // Adiciona o container ao turmasContainer
                turmasContainer.appendChild(divContainer);
            });
        } else {
            turmasContainer.innerHTML = '<p>Nenhuma turma encontrada para esta avaliação</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocorreu um erro ao carregar as turmas');
    });
}