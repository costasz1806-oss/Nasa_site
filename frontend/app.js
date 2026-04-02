/**
 * NASA APOD - Foto do Espaço no Aniversário
 * Frontend - Interface simples para todas as idades
 */

// API na mesma origem (funciona em local e em produção)
const API_URL = 'https://nasa-site-oh6r.onrender.com';
//asdasd
// Elementos do DOM
const inputData = document.getElementById('data-aniversario');
const btnBuscar = document.getElementById('btn-buscar');
const secaoResultado = document.getElementById('resultado');
const divLoading = document.getElementById('loading');
const divConteudo = document.getElementById('conteudo');
const divErro = document.getElementById('erro');

const tituloFoto = document.getElementById('titulo-foto');
const dataExibicao = document.getElementById('data-exibicao');
const imagemApod = document.getElementById('imagem-apod');
const videoApod = document.getElementById('video-apod');
const descricao = document.getElementById('descricao');
const copyright = document.getElementById('copyright');
const mensagemErro = document.getElementById('mensagem-erro');

// Define data máxima como hoje
inputData.max = new Date().toISOString().split('T')[0];

function formatarDataBrasil(dataStr) {
    const [ano, mes, dia] = dataStr.split('-');
    return `${dia}/${mes}/${ano}`;
}

function mostrarEstado(estado) {
    divLoading.hidden = estado !== 'loading';
    divConteudo.hidden = estado !== 'sucesso';
    divErro.hidden = estado !== 'erro';
}

async function buscarFoto() {
    const data = inputData.value;
    
    if (!data) {
        mensagemErro.textContent = 'Por favor, escolha uma data antes de buscar!';
        mostrarEstado('erro');
        secaoResultado.hidden = false;
        return;
    }

    secaoResultado.hidden = false;
    mostrarEstado('loading');
    btnBuscar.disabled = true;

    try {
        const resposta = await fetch(`${API_URL}/apod?api_key=drjSbRBbdgjhVo8wDenwolluSMw5c4bejpvzwZ3E&date=${data}`);
        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.mensagem || 'Algo deu errado. Tente novamente!');
        }

        if (resultado.erro) {
            throw new Error(resultado.mensagem);
        }

        const dados = resultado.data;

        tituloFoto.textContent = dados.titulo;
        dataExibicao.textContent = `Foto do dia ${formatarDataBrasil(dados.data)}`;

        if (dados.tipo_midia === 'video') {
            imagemApod.hidden = true;
            videoApod.hidden = false;
            videoApod.src = dados.url_imagem;
        } else {
            videoApod.hidden = true;
            videoApod.src = '';
            imagemApod.hidden = false;
            imagemApod.src = dados.url_imagem;
            imagemApod.alt = dados.titulo;
        }

        descricao.textContent = dados.descricao;
        copyright.textContent = dados.copyright ? `Créditos: ${dados.copyright}` : '';

        mostrarEstado('sucesso');
    } catch (erro) {
        mensagemErro.textContent = erro.message || 'Não foi possível buscar a foto. Verifique se o servidor está rodando.';
        mostrarEstado('erro');
    } finally {
        btnBuscar.disabled = false;
    }
}

btnBuscar.addEventListener('click', buscarFoto);

inputData.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') buscarFoto();
});
