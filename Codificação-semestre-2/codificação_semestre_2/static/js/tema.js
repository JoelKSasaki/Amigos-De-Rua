/* Compartilha a preferência entre páginas locais e páginas servidas pelo Flask. */
(() => {
  const chave = 'miau-uau-tema';
  const prefixoJanela = `${chave}=`;

  function lerDaJanela() {
    const item = window.name.split('|').find((parte) => parte.startsWith(prefixoJanela));
    return item ? item.slice(prefixoJanela.length) : '';
  }

  function gravarNaJanela(tema) {
    const partes = window.name.split('|').filter((parte) => !parte.startsWith(prefixoJanela));
    partes.push(`${prefixoJanela}${tema}`);
    window.name = partes.filter(Boolean).join('|');
  }

  function obter() {
    const temaDaJanela = lerDaJanela();
    if (location.protocol === 'file:'
      && (temaDaJanela === 'claro' || temaDaJanela === 'escuro')) return temaDaJanela;

    try {
      const salvo = localStorage.getItem(chave);
      if (salvo === 'claro' || salvo === 'escuro') return salvo;
    } catch {
      // Arquivos locais podem não compartilhar o armazenamento do navegador.
    }

    const cookie = document.cookie.match(/(?:^|; )miau-uau-tema=([^;]*)/);
    if (cookie) {
      try {
        const tema = decodeURIComponent(cookie[1]);
        if (tema === 'claro' || tema === 'escuro') return tema;
      } catch {
        // Ignora um cookie inválido e consulta a preferência da aba.
      }
    }

    return temaDaJanela === 'claro' || temaDaJanela === 'escuro' ? temaDaJanela : '';
  }

  function gravar(tema) {
    gravarNaJanela(tema);
    try {
      localStorage.setItem(chave, tema);
    } catch {
      // A preferência continua disponível na navegação da aba.
    }
    document.cookie = `${chave}=${encodeURIComponent(tema)}; path=/; max-age=31536000; samesite=lax`;
  }

  window.miauUauTema = { obter, gravar };
  const tema = obter();
  if (tema) document.documentElement.dataset.tema = tema;
})();
