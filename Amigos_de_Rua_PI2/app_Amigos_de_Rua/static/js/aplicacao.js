/* ==================== Chaves e dados de exemplo ==================== */
const chavePacientes = 'miau-uau-pacientes';
const chaveProcedimentos = 'miau-uau-procedimentos';
const racasDeExemplo = [
  'Bichon Frisé', 'Beagle', 'Border Collie', 'Buldogue Francês',
  'Chihuahua', 'Golden Retriever', 'Labrador Retriever', 'Lhasa Apso',
  'Pastor Alemão', 'Pinscher', 'Poodle', 'Poodle Toy', 'Pug',
  'Shih-tzu', 'Spitz Alemão', 'Yorkshire Terrier', 'Sem raça definida (SRD)'
];

/* ==================== Leitura e gravação dos dados de demonstração ==================== */
function lerLista(chave) {
  try {
    const dados = JSON.parse(localStorage.getItem(chave));
    return Array.isArray(dados) ? dados : null;
  } catch {
    return null;
  }
}

function obterPacientes() {
  let pacientes = lerLista(chavePacientes);
  if (!pacientes) {
    pacientes = pacientesDeExemplo;
    localStorage.setItem(chavePacientes, JSON.stringify(pacientes));
  }
  let alterado = false;
  const codigos = new Set(pacientes.map((paciente) => paciente.codigo).filter(Boolean));
  pacientes = pacientes.map((paciente) => {
    if (paciente.codigo) return paciente;
    let codigo;
    do {
      codigo = `#${String(Math.floor(10000000 + Math.random() * 90000000))}`;
    } while (codigos.has(codigo));
    codigos.add(codigo);
    alterado = true;
    return { ...paciente, codigo };
  });
  if (alterado) gravarPacientes(pacientes);
  return pacientes;
}

function gerarCodigoPaciente(pacientes) {
  const existentes = new Set(pacientes.map((paciente) => paciente.codigo));
  let codigo;
  do {
    codigo = `#${String(Math.floor(10000000 + Math.random() * 90000000))}`;
  } while (existentes.has(codigo));
  return codigo;
}

function obterProcedimentos() {
  let procedimentos = lerLista(chaveProcedimentos);
  if (!procedimentos) {
    procedimentos = procedimentosDeExemplo;
    localStorage.setItem(chaveProcedimentos, JSON.stringify(procedimentos));
  }
  return procedimentos;
}

function gravarPacientes(pacientes) {
  localStorage.setItem(chavePacientes, JSON.stringify(pacientes));
}

function localizarPaciente(identificador) {
  return obterPacientes().find((paciente) => paciente.id === identificador);
}

function localizarProcedimentosDoPaciente(identificador) {
  return obterProcedimentos()
    .filter((procedimento) => procedimento.idPaciente === identificador)
    .sort((primeiro, segundo) => new Date(segundo.data) - new Date(primeiro.data));
}

function formatarData(data) {
  if (!data) return 'Sem registros';
  return new Date(data).toLocaleDateString('pt-BR');
}

function formatarDataHora(data) {
  if (!data) return 'Data não informada';
  const horario = new Date(data);
  return `${horario.toLocaleDateString('pt-BR')} às ${horario.toLocaleTimeString('pt-BR', {
    hour: '2-digit', minute: '2-digit'
  })}`;
}

function obterTemaSalvo() {
  return window.miauUauTema?.obter() || 'claro';
}

function gravarTemaSalvo(tema) {
  window.miauUauTema?.gravar(tema);
}

/* ==================== Modo claro e modo noturno persistente ==================== */
function configurarTema() {
  const raiz = document.documentElement;
  const botoesTema = document.querySelectorAll('[data-alternar-tema]');

  function aplicarTema(tema) {
    raiz.dataset.tema = tema;
    gravarTemaSalvo(tema);
    botoesTema.forEach((botao) => {
      const modoEscuro = tema === 'escuro';
      botao.setAttribute('aria-label', modoEscuro ? 'Ativar modo claro' : 'Ativar modo noturno');
      botao.innerHTML = modoEscuro
        ? '<span aria-hidden="true">☀</span><span class="texto-tema">Modo claro</span>'
        : '<span aria-hidden="true">☾</span><span class="texto-tema">Modo noturno</span>';
    });
  }

  aplicarTema(obterTemaSalvo());
  botoesTema.forEach((botao) => {
    botao.addEventListener('click', () => {
      aplicarTema(raiz.dataset.tema === 'escuro' ? 'claro' : 'escuro');
    });
  });
}

/* ==================== Funções para montar elementos com segurança ==================== */
function criarElemento(tag, classe, texto) {
  const elemento = document.createElement(tag);
  if (classe) elemento.className = classe;
  if (texto !== undefined) elemento.textContent = texto;
  return elemento;
}

async function copiarTexto(texto) {
  try {
    await navigator.clipboard.writeText(texto);
    return true;
  } catch {
    const campoTemporario = document.createElement('textarea');
    campoTemporario.value = texto;
    campoTemporario.style.position = 'fixed';
    campoTemporario.style.opacity = '0';
    document.body.append(campoTemporario);
    campoTemporario.select();
    const copiado = document.execCommand('copy');
    campoTemporario.remove();
    return copiado;
  }
}

function tornarCopiavel(elemento, texto) {
  elemento.setAttribute('role', 'button');
  elemento.setAttribute('tabindex', '0');
  elemento.setAttribute('aria-label', `Copiar ID ${texto}`);

  const copiar = async (evento) => {
    evento.preventDefault();
    evento.stopPropagation();
    if (!await copiarTexto(texto)) return;

    elemento.textContent = 'Copiado!';
    elemento.setAttribute('aria-label', `ID ${texto} copiado`);
    window.setTimeout(() => {
      elemento.textContent = texto;
      elemento.setAttribute('aria-label', `Copiar ID ${texto}`);
    }, 1200);
  };

  elemento.addEventListener('click', copiar);
  elemento.addEventListener('keydown', (evento) => {
    if (evento.key === 'Enter' || evento.key === ' ') copiar(evento);
  });
}

function classeDoAvatar(icone) {
  if (icone === '🐕') return 'avatar-areia';
  if (icone === '🐩') return 'avatar-mel';
  if (icone === '🐾') return 'avatar-lilas';
  return 'avatar-creme';
}

/* ==================== Cartões e busca do painel inicial ==================== */
function criarCartaoPaciente(paciente) {
  const cartao = criarElemento('a', 'cartao-paciente');
  cartao.href = `/ficha-pet?id=${encodeURIComponent(paciente.id)}`;
  cartao.dataset.busca = [paciente.nome, paciente.raca, paciente.codigo, paciente.id]
    .join(' ').toLocaleLowerCase('pt-BR');

  const resumo = criarElemento('div', 'resumo-paciente');
  const foto = criarElemento('span', 'foto-paciente-cartao');
  const icone = criarElemento(
    'span', `avatar-paciente ${classeDoAvatar(paciente.icone)}`, paciente.icone || '🐶'
  );
  icone.setAttribute('aria-hidden', 'true');
  const sexo = paciente.sexo === 'Fêmea' ? '♀' : paciente.sexo === 'Macho' ? '♂' : '';
  foto.append(icone);
  if (sexo) {
    const classeSexo = paciente.sexo === 'Fêmea' ? 'sexo-femea' : 'sexo-macho';
    const indicadorSexo = criarElemento('span', `icone-sexo-card ${classeSexo}`, sexo);
    indicadorSexo.setAttribute('aria-label', paciente.sexo);
    foto.append(indicadorSexo);
  }
  const dados = criarElemento('div', 'dados-paciente');
  dados.append(criarElemento('h3', '', paciente.nome));
  dados.append(criarElemento('p', '', paciente.raca || 'Raça não informada'));
  dados.append(criarElemento('span', 'texto-abrir-ficha', 'Acessar ficha ›'));
  const codigoPaciente = paciente.codigo || paciente.id;
  const identificador = criarElemento('span', 'identificador-cartao-paciente', codigoPaciente);
  tornarCopiavel(identificador, codigoPaciente);
  resumo.append(foto, dados);

  const metadados = criarElemento('div', 'metadados-paciente');
  const tutor = criarElemento('div');
  tutor.append(criarElemento('small', '', 'TUTOR'));
  tutor.append(criarElemento('b', '', paciente.tutor));
  const ultimo = localizarProcedimentosDoPaciente(paciente.id)[0];
  const procedimento = criarElemento('div');
  procedimento.append(criarElemento('small', '', 'ÚLTIMO PROCEDIMENTO'));
  procedimento.append(criarElemento('b', '', formatarData(ultimo?.data)));
  metadados.append(tutor, procedimento);
  cartao.append(identificador, resumo, metadados);
  return cartao;
}

function configurarPainel() {
  const grade = document.querySelector('#grade-pacientes');
  if (!grade) return;

  const busca = document.querySelector('#busca-pacientes');
  const mensagemVazia = document.querySelector('#mensagem-sem-pacientes');
  const pacientes = obterPacientes();

  function renderizarCartoes(termo = '') {
    const consulta = termo.trim().toLocaleLowerCase('pt-BR');
    const encontrados = pacientes.filter((paciente) => {
      const conteudo = [paciente.nome, paciente.raca, paciente.codigo, paciente.id]
        .join(' ').toLocaleLowerCase('pt-BR');
      return conteudo.includes(consulta);
    }).slice(0,6);
    grade.replaceChildren(...encontrados.map(criarCartaoPaciente));
    mensagemVazia.hidden = encontrados.length > 0;
  }

  renderizarCartoes();
  busca.addEventListener('input', () => renderizarCartoes(busca.value));

  const campoData = document.querySelector('[data-data-atual]');
  if (campoData) {
    campoData.textContent = new Date().toLocaleDateString('pt-BR', {
      day: 'numeric', month: 'short'
    });
  }
}

/* ==================== Duas colunas de procedimentos recentes no painel ==================== */
function criarCartaoProcedimentoRecente(procedimento) {
  const paciente = localizarPaciente(procedimento.idPaciente);
  const cartao = criarElemento('a', 'cartao-procedimento-recente');
  cartao.href = `/ficha-pet?id=${encodeURIComponent(procedimento.idPaciente)}`;

  const topo = criarElemento('div', 'topo-procedimento-recente');
  const identificador = criarElemento('span', 'id-procedimento-recente', procedimento.id);
  tornarCopiavel(identificador, procedimento.id);
  topo.append(identificador);
  topo.append(criarElemento('time', 'data-procedimento-recente', formatarDataHora(procedimento.data)));
  cartao.append(topo);
  cartao.append(criarElemento('p', 'nome-paciente-recente', paciente?.nome || 'Cadastro removido'));
  cartao.append(criarElemento('p', 'tipo-procedimento-recente', (procedimento.tipos || []).join(' · ')));
  return cartao;
}

function configurarProcedimentosRecentes() {
  const grade = document.querySelector('#grade-procedimentos-recentes');
  if (!grade) return;
  const mensagemVazia = document.querySelector('#mensagem-sem-procedimento-recente');
  const recentes = [...obterProcedimentos()]
    .sort((primeiro, segundo) => new Date(segundo.data) - new Date(primeiro.data))
    .slice(0, 4);
  grade.replaceChildren(...recentes.map(criarCartaoProcedimentoRecente));
  grade.hidden = recentes.length === 0;
  mensagemVazia.hidden = recentes.length > 0;
}

/* ==================== Sugestões de raça para o cadastro ==================== */
function configurarSugestoesDeRaca() {
  const lista = document.querySelector('#lista-racas');
  if (!lista) return;
  const opcoes = racasDeExemplo.map((raca) => {
    const opcao = document.createElement('option');
    opcao.value = raca;
    return opcao;
  });
  lista.replaceChildren(...opcoes);
}

/* ==================== Cadastro novo e edição de dados ==================== */
function preencherFormulario(formulario, paciente) {
  Object.entries(paciente).forEach(([nome, valor]) => {
    const campos = formulario.querySelectorAll(`[name="${nome}"]`);
    campos.forEach((campo) => {
      if (campo.type === 'radio') campo.checked = campo.value === valor;
      else if (campo.type !== 'file') campo.value = valor ?? '';
    });
  });
}

function lerFormulario(formulario) {
  const dados = Object.fromEntries(new FormData(formulario).entries());
  dados.icone = formulario.querySelector('[name="icone"]:checked')?.value || '🐶';
  return dados;
}

function configurarCadastro() {
  const formulario = document.querySelector('#formulario-cadastro');
  if (!formulario) return;

  configurarSugestoesDeRaca();
  const parametros = new URLSearchParams(window.location.search);
  const identificador = parametros.get('id');
  const paciente = identificador ? localizarPaciente(identificador) : null;
  const titulo = document.querySelector('#titulo-cadastro');
  const botaoSalvar = document.querySelector('#botao-salvar-cadastro');
  const mensagem = document.querySelector('#aviso-cadastro');

  if (paciente) {
    preencherFormulario(formulario, paciente);
    titulo.textContent = `Editar cadastro de ${paciente.nome}`;
    botaoSalvar.textContent = 'Salvar alterações';
  } else if (identificador) {
    titulo.textContent = 'Cadastro não encontrado';
    mensagem.textContent = 'Este paciente não está nos cadastros disponíveis.';
    botaoSalvar.disabled = true;
  }

  const campoCpf = formulario.elements.cpf;
  campoCpf.addEventListener('input', () => {
    const numeros = campoCpf.value.replace(/\D/g, '').slice(0, 11);
    campoCpf.value = numeros
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  });

  formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();
    if (!formulario.reportValidity()) return;

    const dados = lerFormulario(formulario);

    // Edição de pet existente: ainda só local (será ligada ao banco numa próxima etapa)
    if (paciente) {
      const pacientes = obterPacientes();
      gravarPacientes(pacientes.map((item) => item.id === paciente.id
        ? { ...item, ...dados, id: paciente.id, codigo: paciente.codigo, criadoEm: item.criadoEm }
        : item));
      window.location.href = `/ficha-pet?id=${encodeURIComponent(paciente.id)}&salvo=1`;
      return;
    }

    // Pet novo: grava no Supabase através do Flask
    botaoSalvar.disabled = true;
    mensagem.textContent = 'Salvando...';
    try {
      const resposta = await fetch('/api/pets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
      });
      const resultado = await resposta.json();
      if (!resposta.ok) throw new Error(resultado.erro || 'Erro ao salvar');
      window.location.href = `/ficha-pet?id=${encodeURIComponent(resultado.id)}&novo=1`;
    } catch (erro) {
      mensagem.textContent = 'Não foi possível salvar: ' + erro.message;
      botaoSalvar.disabled = false;
    }
  });
}

/* ==================== Ficha completa e histórico recente ==================== */
function criarCartaoHistorico(procedimento) {
  const cartao = criarElemento('article', 'cartao-historico');
  const cabecalho = criarElemento('div', 'cabecalho-historico');
  cartao.dataset.idProcedimento = procedimento.id;

  const resumo = criarElemento('div', 'resumo-historico');
  resumo.append(criarElemento('time', 'data-historico', formatarDataHora(procedimento.data)));
  const tipos = criarElemento('div', 'tipos-historico');
  (procedimento.tipos || []).forEach((tipo) => {
    tipos.append(criarElemento('div', 'linha-tipo-historico', tipo));
  });
  resumo.append(tipos);

  const botaoRecolher = criarElemento('button', 'botao-recolher-historico');
  botaoRecolher.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 14 5-4 5 4" /></svg>';
  botaoRecolher.type = 'button';
  botaoRecolher.setAttribute('aria-expanded', 'true');
  botaoRecolher.setAttribute('aria-label', 'Recolher detalhes do procedimento');
  cabecalho.append(resumo, botaoRecolher);

  const detalhes = criarElemento('div', 'detalhes-historico');
  const campos = [
    ['Profissional responsável', procedimento.profissional || 'Não informado', '', 'rotulo-profissional'],
    ['Descrição do procedimento', procedimento.descricao || 'Sem descrição.', '', 'rotulo-descricao'],
    ['Observações', procedimento.observacoes || 'Nenhuma.', '', 'rotulo-observacoes']
  ];
  campos.forEach(([rotulo, valor, classeValor, classeRotulo]) => {
    const campo = criarElemento('div', 'campo-historico');
    campo.append(criarElemento('div', `rotulo-historico ${classeRotulo}`, rotulo));
    campo.append(criarElemento('div', `valor-historico ${classeValor || ''}`, valor));
    detalhes.append(campo);
  });

  botaoRecolher.addEventListener('click', () => {
    const aberto = botaoRecolher.getAttribute('aria-expanded') === 'true';
    botaoRecolher.setAttribute('aria-expanded', String(!aberto));
    botaoRecolher.setAttribute('aria-label', aberto
      ? 'Expandir detalhes do procedimento'
      : 'Recolher detalhes do procedimento');
    botaoRecolher.innerHTML = aberto
      ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 10 5 4 5-4" /></svg>'
      : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m7 14 5-4 5 4" /></svg>';
    detalhes.hidden = aberto;
  });

  cartao.append(cabecalho, detalhes);
  return cartao;
}

function configurarFicha() {
  const pagina = document.querySelector('[data-pagina="ficha"]');
  if (!pagina) return;

  const parametros = new URLSearchParams(window.location.search);
  const paciente = localizarPaciente(parametros.get('id'));
  const aviso = document.querySelector('#aviso-ficha');
  if (!paciente) {
    document.querySelector('#conteudo-ficha').hidden = true;
    aviso.textContent = 'Cadastro do paciente não encontrado.';
    return;
  }

  document.querySelector('#icone-ficha').textContent = paciente.icone || '🐶';
  document.querySelector('#icone-ficha').className =
    `avatar-paciente ${classeDoAvatar(paciente.icone)}`;
  document.querySelector('#nome-ficha').textContent = paciente.nome;
  document.querySelector('#subtitulo-ficha').textContent =
    `${paciente.raca || 'Raça não informada'} · Porte ${paciente.porte || 'não informado'}`;
  document.querySelector('#id-ficha').textContent = paciente.codigo || paciente.id;

  const condicaoReprodutiva = paciente.castrado === 'Sim'
    ? `Sim (${paciente.sexo === 'Fêmea' ? 'castrada' : 'castrado'})`
    : paciente.castrado === 'Não'
      ? `Não (não ${paciente.sexo === 'Fêmea' ? 'castrada' : 'castrado'})`
      : 'Não informado';
  const valores = {
    raca: paciente.raca, porte: paciente.porte, peso: paciente.peso,
    idade: paciente.idade, sexo: paciente.sexo, cor: paciente.cor,
    castrado: condicaoReprodutiva, alergias: paciente.alergias,
    tutor: paciente.tutor, cpf: paciente.cpf, nis: paciente.nis, telefone: paciente.telefone,
    endereco: paciente.endereco
  };
  Object.entries(valores).forEach(([campo, valor]) => {
    const destino = document.querySelector(`[data-dado="${campo}"]`);
    if (destino) destino.textContent = valor || 'Não informado';
  });

  const idCodificado = encodeURIComponent(paciente.id);
  document.querySelector('#botao-editar-ficha').href = `/cadastrar-pet?id=	${idCodificado}`;
  document.querySelector('#botao-novo-procedimento-ficha').href = `/novo-procedimento?id=${idCodificado}`;
  document.querySelector('#botao-ver-procedimentos').href = `/todos-procedimentos?idPaciente=${idCodificado}`;

  const procedimentos = localizarProcedimentosDoPaciente(paciente.id);
  const recentes = procedimentos.slice(0, 5);
  document.querySelector('#contagem-procedimentos').textContent = procedimentos.length;
  const lista = document.querySelector('#lista-historico');
  lista.replaceChildren(...recentes.map(criarCartaoHistorico));
  document.querySelector('#mensagem-sem-historico').hidden = procedimentos.length > 0;

  if (parametros.has('salvo')) aviso.textContent = 'Dados do cadastro atualizados.';
  if (parametros.has('novo')) aviso.textContent = 'Cadastro criado com sucesso.';
  if (parametros.has('procedimento')) aviso.textContent = 'Procedimento registrado com sucesso.';
}

/* ==================== Lista de todos os cadastros e filtros ==================== */
function configurarTodosCadastros() {
  const lista = document.querySelector('#lista-todos-pacientes');
  if (!lista) return;

  const busca = document.querySelector('#busca-todos-pacientes');
  const ordem = document.querySelector('#ordem-pacientes');
  const mensagem = document.querySelector('#mensagem-sem-pacientes');
  const contagem = document.querySelector('#contagem-todos-pacientes');
  const limpar = document.querySelector('#limpar-filtros-cadastros');
  const filtros = { sexo: '', porte: '', castracao: '' };
  const gruposFiltro = [...document.querySelectorAll('.grupo-segmentado')];

  function renderizar() {
    const termo = busca.value.trim().toLocaleLowerCase('pt-BR');
    const pacientes = obterPacientes().filter((paciente) =>
      `${paciente.codigo} ${paciente.id} ${paciente.nome} ${paciente.raca}`.toLocaleLowerCase('pt-BR').includes(termo)
      && (!filtros.sexo || paciente.sexo === filtros.sexo)
      && (!filtros.porte || paciente.porte === filtros.porte)
      && (!filtros.castracao || paciente.castrado === filtros.castracao)
    );
    pacientes.sort((primeiro, segundo) => {
      const dataPrimeiro = localizarProcedimentosDoPaciente(primeiro.id)[0]?.data || primeiro.criadoEm || '';
      const dataSegundo = localizarProcedimentosDoPaciente(segundo.id)[0]?.data || segundo.criadoEm || '';
      return ordem.value === 'antigos'
        ? new Date(dataPrimeiro) - new Date(dataSegundo)
        : new Date(dataSegundo) - new Date(dataPrimeiro);
    });
    lista.replaceChildren(...pacientes.map(criarCartaoPaciente));
    mensagem.hidden = pacientes.length > 0;
    contagem.textContent = `Exibindo ${pacientes.length} ${pacientes.length === 1 ? 'cão encontrado' : 'cães encontrados'}`;
  }

  busca.addEventListener('input', renderizar);
  ordem.addEventListener('change', renderizar);
  gruposFiltro.forEach((grupo) => {
    grupo.addEventListener('click', (evento) => {
      const botao = evento.target.closest('button[data-valor]');
      if (!botao) return;
      const tipo = grupo.dataset.filtro;
      filtros[tipo] = botao.dataset.valor;
      grupo.querySelectorAll('button[data-valor]').forEach((opcao) => {
        opcao.setAttribute('aria-pressed', String(opcao === botao));
      });
      renderizar();
    });
  });
  limpar.addEventListener('click', () => {
    busca.value = '';
    Object.keys(filtros).forEach((tipo) => { filtros[tipo] = ''; });
    gruposFiltro.forEach((grupo) => {
      grupo.querySelectorAll('button[data-valor]').forEach((botao) => {
        botao.setAttribute('aria-pressed', String(botao.dataset.valor === ''));
      });
    });
    ordem.value = 'recentes';
    renderizar();
  });
  renderizar();
}

/* ==================== Lista de procedimentos e filtros ==================== */
function criarLinhaProcedimento(procedimento) {
  const paciente = localizarPaciente(procedimento.idPaciente);
  const cartao = criarElemento('a', 'cartao-procedimento');
  cartao.href = `/ficha-pet?id=${encodeURIComponent(procedimento.idPaciente)}`;
  const topo = criarElemento('div', 'cabecalho-historico');
  const identificador = criarElemento('span', 'identificador-procedimento', procedimento.id);
  tornarCopiavel(identificador, procedimento.id);
  topo.append(identificador);
  topo.append(criarElemento('time', 'data-historico', formatarDataHora(procedimento.data)));
  cartao.append(topo);
  cartao.append(criarElemento('h2', '', (procedimento.tipos || []).join(' · ')));
  cartao.append(criarElemento('p', 'texto-historico', `Paciente: ${paciente?.nome || 'Cadastro removido'}`));
  cartao.append(criarElemento('p', 'texto-historico', `ID do cachorro: ${paciente?.codigo || procedimento.idPaciente}`));
  cartao.append(criarElemento('p', 'texto-historico', `Responsável: ${procedimento.profissional || 'Não informado'}`));
  return cartao;
}

function configurarTodosProcedimentos() {
  const lista = document.querySelector('#lista-todos-procedimentos');
  if (!lista) return;

  const busca = document.querySelector('#busca-todos-procedimentos');
  const filtroTipo = document.querySelector('#filtro-tipo-procedimento');
  const filtroPet = new URLSearchParams(window.location.search).get('idPaciente');
  const avisoFiltro = document.querySelector('#aviso-filtro-paciente');
  const mensagem = document.querySelector('#mensagem-sem-procedimentos');
  if (filtroPet) {
    const paciente = localizarPaciente(filtroPet);
    avisoFiltro.hidden = false;
    avisoFiltro.textContent = paciente
      ? `Mostrando somente procedimentos de ${paciente.nome} (${paciente.codigo || paciente.id}).`
      : `Mostrando somente procedimentos do cadastro ${filtroPet}.`;
  }

  function renderizar() {
    const termo = busca.value.trim().toLocaleLowerCase('pt-BR');
    const procedimentos = obterProcedimentos()
      .filter((procedimento) => !filtroPet || procedimento.idPaciente === filtroPet)
      .filter((procedimento) => !filtroTipo.value
        || (procedimento.tipos || []).includes(filtroTipo.value))
      .filter((procedimento) => {
        const paciente = localizarPaciente(procedimento.idPaciente);
        const conteudo = [
          procedimento.id, paciente?.nome, paciente?.codigo, procedimento.idPaciente
        ].join(' ').toLocaleLowerCase('pt-BR');
        return conteudo.includes(termo);
      })
      .sort((primeiro, segundo) => new Date(segundo.data) - new Date(primeiro.data));
    lista.replaceChildren(...procedimentos.map(criarLinhaProcedimento));
    mensagem.hidden = procedimentos.length > 0;
  }

  busca.addEventListener('input', renderizar);
  filtroTipo.addEventListener('change', renderizar);
  renderizar();
}

/* ==================== Criação de procedimento com checklist ==================== */
function configurarProcedimento() {
  const formulario = document.querySelector('#formulario-procedimento');
  if (!formulario) return;

  const pacientes = obterPacientes();
  const parametros = new URLSearchParams(window.location.search);
  const identificadorInicial = parametros.get('id');
  const seletor = document.querySelector('#seletor-paciente');
  const campoSeletor = document.querySelector('#campo-selecionar-paciente');
  const painelPaciente = document.querySelector('#paciente-selecionado');
  const mensagem = document.querySelector('#aviso-procedimento');
  const codigoPaciente = document.querySelector('#codigo-paciente-procedimento');
  codigoPaciente.addEventListener('click', async () => {
    const codigo = codigoPaciente.dataset.codigo;
    if (!codigo) return;
    if (!await copiarTexto(codigo)) return;
    codigoPaciente.textContent = 'Copiado!';
    codigoPaciente.setAttribute('aria-label', `ID ${codigo} copiado`);
    window.setTimeout(() => {
      codigoPaciente.textContent = codigo;
      codigoPaciente.setAttribute('aria-label', `Copiar ID ${codigo}`);
    }, 1200);
  });
  const dataAtendimento = formulario.elements.data;
  const agora = new Date();
  const deslocamento = agora.getTimezoneOffset() * 60000;
  dataAtendimento.value = new Date(agora.getTime() - deslocamento).toISOString().slice(0, 16);

  pacientes.forEach((paciente) => {
    const opcao = document.createElement('option');
    opcao.value = paciente.id;
    opcao.textContent = `${paciente.nome} · ${paciente.raca || 'Raça não informada'}`;
    seletor.append(opcao);
  });

  function atualizarPacienteSelecionado(identificador) {
    const paciente = localizarPaciente(identificador);
    if (!paciente) {
      painelPaciente.hidden = true;
      campoSeletor.hidden = false;
      return;
    }
    seletor.value = paciente.id;
    campoSeletor.hidden = true;
    painelPaciente.hidden = false;
    const icone = document.querySelector('#icone-paciente-procedimento');
    icone.textContent = paciente.icone || '🐶';
    icone.className = `avatar-paciente ${classeDoAvatar(paciente.icone)}`;
    document.querySelector('#nome-paciente-procedimento').textContent = paciente.nome;
    codigoPaciente.textContent = paciente.codigo || paciente.id;
    codigoPaciente.dataset.codigo = paciente.codigo || paciente.id;
    document.querySelector('#detalhes-paciente-procedimento').textContent =
      `${paciente.raca || 'Raça não informada'} · Porte ${paciente.porte || 'não informado'}`;
    document.querySelector('#link-ficha-paciente').href =
      `/ficha-pet?id=${encodeURIComponent(paciente.id)}`;
    document.querySelector('#voltar-do-procedimento').href =
      `/ficha-pet?id=${encodeURIComponent(paciente.id)}`;
    document.querySelector('#cancelar-procedimento').href =
      `/ficha-pet?id=${encodeURIComponent(paciente.id)}`;
  }

  if (identificadorInicial) atualizarPacienteSelecionado(identificadorInicial);
  seletor.addEventListener('change', () => atualizarPacienteSelecionado(seletor.value));

  formulario.querySelectorAll('textarea[maxlength]').forEach((campo) => {
    const contador = document.querySelector(`[data-contador="${campo.name}"]`);
    const atualizarContagem = () => {
      contador.textContent = `${campo.value.length} de ${campo.maxLength} caracteres`;
    };
    campo.addEventListener('input', atualizarContagem);
    atualizarContagem();
  });

  formulario.addEventListener('submit', (evento) => {
    evento.preventDefault();
    if (!formulario.reportValidity()) return;

    const tipos = [...formulario.querySelectorAll('[name="tipos"]:checked')]
      .map((campo) => campo.value);
    if (tipos.length === 0) {
      mensagem.textContent = 'Marque pelo menos um tipo de procedimento.';
      formulario.querySelector('[name="tipos"]')?.focus();
      return;
    }

    const dados = Object.fromEntries(new FormData(formulario).entries());
    dados.tipos = tipos;
    dados.id = `procedimento-${Date.now()}`;
    dados.idPaciente = seletor.value;
    dados.fotoAntes = formulario.elements['foto-antes'].files[0]?.name || '';
    dados.fotoDepois = formulario.elements['foto-depois'].files[0]?.name || '';
    delete dados['foto-antes'];
    delete dados['foto-depois'];
    const registros = obterProcedimentos();
    registros.push(dados);
    localStorage.setItem(chaveProcedimentos, JSON.stringify(registros));
    window.location.href = `/ficha-pet?id=${encodeURIComponent(dados.idPaciente)}&procedimento=salvo`;
  });
}

/* ==================== Carregar os pets do banco (Supabase) ==================== */
async function carregarPetsDoBanco() {
  try {
    const resposta = await fetch('/api/pets');
    if (!resposta.ok) throw new Error('Resposta ' + resposta.status);
    const pets = await resposta.json();
    gravarPacientes(pets);
  } catch (erro) {
    console.error('Não foi possível carregar os pets do banco:', erro);
  }
}

/* ==================== Inicialização dos componentes desta página ==================== */
async function iniciar() {
  configurarTema();
  await carregarPetsDoBanco();
  configurarPainel();
  configurarProcedimentosRecentes();
  configurarCadastro();
  configurarFicha();
  configurarTodosCadastros();
  configurarTodosProcedimentos();
  configurarProcedimento();
}

iniciar();
