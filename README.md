# Loja do Neoveg

Catálogo de scripts e extensões para o [Neoveg](https://github.com/LARPFX-ori/neoveg). O Neoveg baixa o `index.json` deste repositório, mostra os pacotes na janela **Loja** e instala o que você escolher, conferindo o SHA-256 de cada arquivo antes de gravar.

## O que tem aqui

| Pasta ou arquivo | Conteúdo |
| --- | --- |
| `pacotes/<id>/` | Um pacote: o `pacote.json` e os arquivos dele |
| `index.json` | Catálogo gerado a partir de `pacotes/`; é o que o programa lê |
| `ferramentas/loja.py` | Valida os pacotes e gera o `index.json` |
| `index.html` | Página da loja (GitHub Pages): <https://larpfx-ori.github.io/neoveg-marketplace/> |

## Regras

- **Só código-fonte.** Scripts C# (`.cs`), Python (`.py`) e extensões, com textos e imagens. Nada de `.exe`, `.dll`, instaladores ou arquivos compactados.
- **Só licenças permitidas.** As mesmas do Neoveg: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, OFL-1.1, Ubuntu-font-1.0, Bitstream-Vera, CC0-1.0, CC-BY-4.0, CC-BY-SA-4.0 e LicenseRef-Public-Domain.
- **Scripts de terceiros** entram com a licença e o endereço do original em `fonte`, e sem os programas externos que eles chamem.
- **Limites:** 1 MiB por arquivo, 5 MiB e 64 arquivos por pacote.

A CI roda `python ferramentas/loja.py validar` em todo pull request e recusa o pacote que quebrar uma regra.

## Formato do `pacote.json`

```json
{
  "id": "marcadores-a-cada-intervalo",
  "nome": "Marcadores a cada intervalo",
  "descricao": "Põe um marcador a cada 5 segundos.",
  "versao": "1.0.0",
  "tipo": "script-cs",
  "autor": "Contribuidores do Neoveg",
  "licenca": "MIT OR Apache-2.0",
  "fonte": "original",
  "neoveg_min": "0.2.0",
  "entrada": "MarcadoresACadaIntervalo.cs",
  "arquivos": ["MarcadoresACadaIntervalo.cs"],
  "tags": ["marcadores"]
}
```

- `id`: igual ao nome da pasta, em minúsculas com hífens.
- `tipo`: `script-cs`, `script-py` ou `extensao`.
- `licenca`: um identificador SPDX da lista, ou uma expressão com `OR`/`AND`.
- `fonte`: `original` ou o endereço `https://` do projeto de origem.
- `neoveg_min`: a versão mais antiga do Neoveg em que o pacote funciona.
- `entrada`: o arquivo que o Neoveg executa.
- `arquivos`: todos os arquivos da pasta, fora o `pacote.json`.

## Enviar um pacote

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

A estrutura e as ferramentas deste repositório são distribuídas sob `MIT OR Apache-2.0` ([LICENSE-MIT](LICENSE-MIT), [LICENSE-APACHE](LICENSE-APACHE)). Cada pacote tem a licença declarada no seu `pacote.json`.
