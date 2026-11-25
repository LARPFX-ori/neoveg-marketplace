# AGENTS.md — Loja do Neoveg

Valem as Regras da Casa do Neoveg (ver o `AGENTS.md` do repositório principal). Neste repositório também:

1. **`main` muda só por pull request**, com a CI verde.
2. **Nunca apague branches.**
3. **Sem atribuição a agentes** em commits e pull requests.
4. **Só código-fonte com licença da lista** do README; nenhum binário entra, nem dentro de outro arquivo.
5. **O `index.json` é gerado**, nunca editado à mão: `python ferramentas/loja.py gerar`.
6. **Mudar o formato do catálogo** (campos, `versao_formato`) exige mudança junto no Neoveg; aumente `VERSAO_FORMATO` quando a mudança não for compatível.
