# Como enviar um pacote

1. Crie a pasta `pacotes/<id>/` com os arquivos e o `pacote.json` (formato no [README](README.md)).
2. Teste o script no Neoveg (**Ferramentas > Executar script...**) com a versão indicada em `neoveg_min`.
3. Rode `python ferramentas/loja.py gerar` para atualizar o `index.json`, e depois `python ferramentas/loja.py validar`.
4. Abra um pull request com a pasta e o `index.json`. Diga no texto o que o script faz e em que versão do Neoveg você testou.

Para publicar uma versão nova, aumente `versao` no `pacote.json` e gere o índice de novo: o Neoveg mostra a atualização para quem já instalou.

## O que é recusado

- Executáveis, bibliotecas compiladas, instaladores e arquivos compactados.
- Licença fora da lista do README ou sem licença.
- Código copiado sem a licença do original.
- Scripts que baixam e executam programas, apagam arquivos fora do projeto ou mandam dados para a internet sem dizer isso na `descricao`.
