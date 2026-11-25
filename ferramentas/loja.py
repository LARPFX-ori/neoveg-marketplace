#!/usr/bin/env python3
"""Ferramenta do catálogo da Loja do Neoveg.

    python ferramentas/loja.py validar   confere todos os pacotes e o index.json
    python ferramentas/loja.py gerar     regrava o index.json a partir de pacotes/

O `index.json` é o que o Neoveg baixa. Ele lista cada pacote com os arquivos,
o tamanho e o SHA-256 de cada um; o programa confere o hash antes de instalar.
Só a biblioteca padrão do Python 3.11+ é usada.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACOTES = RAIZ / "pacotes"
INDICE = RAIZ / "index.json"
VERSAO_FORMATO = 1

# Lista de licenças permitidas (a mesma do AGENTS.md do Neoveg)
LICENCAS = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "OFL-1.1",
    "Ubuntu-font-1.0",
    "Bitstream-Vera",
    "CC0-1.0",
    "CC-BY-4.0",
    "CC-BY-SA-4.0",
    "LicenseRef-Public-Domain",
}
TIPOS = {"script-cs", "script-py", "extensao"}
# só código-fonte, texto e imagens; nada executável
EXTENSOES = {".cs", ".py", ".md", ".txt", ".json", ".config", ".xml", ".png", ".svg"}
ENTRADA_POR_TIPO = {"script-cs": ".cs", "script-py": ".py", "extensao": ".json"}
ASSINATURAS_BINARIAS = (b"MZ", b"\x7fELF", b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"PK\x03\x04")
MAX_ARQUIVO = 1 << 20  # 1 MiB
MAX_PACOTE = 5 << 20  # 5 MiB
MAX_ARQUIVOS = 64
RE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RE_VERSAO = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
RE_CAMINHO = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$")
CAMPOS = {
    "id": str,
    "nome": str,
    "descricao": str,
    "versao": str,
    "tipo": str,
    "autor": str,
    "licenca": str,
    "fonte": str,
    "neoveg_min": str,
    "entrada": str,
    "arquivos": list,
    "tags": list,
}


def licenca_valida(expr: str) -> bool:
    """Aceita `A`, `A OR B` e `A AND B` com identificadores da lista."""
    partes = re.split(r"\s+(?:OR|AND)\s+", expr.strip())
    return bool(expr.strip()) and all(p in LICENCAS for p in partes)


def sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def validar_pacote(pasta: Path) -> tuple[dict | None, list[str]]:
    erros: list[str] = []
    nome = pasta.name

    def erro(msg: str) -> None:
        erros.append(f"{nome}: {msg}")

    manifesto = pasta / "pacote.json"
    if not manifesto.is_file():
        erro("falta pacote.json")
        return None, erros
    try:
        m = json.loads(manifesto.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        erro(f"pacote.json inválido: {e}")
        return None, erros
    if not isinstance(m, dict):
        erro("pacote.json precisa ser um objeto")
        return None, erros
    for campo, tipo in CAMPOS.items():
        if not isinstance(m.get(campo), tipo):
            erro(f"campo '{campo}' ausente ou com tipo errado")
    extras = set(m) - set(CAMPOS)
    if extras:
        erro(f"campos desconhecidos: {', '.join(sorted(extras))}")
    if erros:
        return None, erros

    if m["id"] != nome or not RE_ID.match(m["id"]):
        erro("o id precisa ser igual ao nome da pasta (minúsculas, números e hífens)")
    for campo in ("versao", "neoveg_min"):
        if not RE_VERSAO.match(m[campo]):
            erro(f"'{campo}' precisa ser uma versão X.Y.Z")
    if m["tipo"] not in TIPOS:
        erro(f"tipo '{m['tipo']}' desconhecido (use {', '.join(sorted(TIPOS))})")
    if not licenca_valida(m["licenca"]):
        erro(f"licença '{m['licenca']}' fora da lista permitida")
    if m["fonte"] != "original" and not m["fonte"].startswith("https://"):
        erro("'fonte' precisa ser 'original' ou um endereço https://")
    for campo, limite in (("nome", 80), ("descricao", 400), ("autor", 120)):
        if not m[campo].strip() or len(m[campo]) > limite:
            erro(f"'{campo}' vazio ou com mais de {limite} caracteres")
    if len(m["tags"]) > 8 or not all(isinstance(t, str) and RE_ID.match(t) for t in m["tags"]):
        erro("'tags': até 8, em minúsculas com hífens")

    arquivos = m["arquivos"]
    if not arquivos or len(arquivos) > MAX_ARQUIVOS:
        erro(f"'arquivos' precisa ter de 1 a {MAX_ARQUIVOS} itens")
    if len(set(arquivos)) != len(arquivos):
        erro("'arquivos' tem itens repetidos")
    if m["entrada"] not in arquivos:
        erro("'entrada' precisa estar em 'arquivos'")
    esperado = ENTRADA_POR_TIPO.get(m["tipo"])
    if esperado and not m["entrada"].endswith(esperado):
        erro(f"a entrada de um pacote '{m['tipo']}' termina em {esperado}")

    presentes = {
        p.relative_to(pasta).as_posix()
        for p in pasta.rglob("*")
        if p.is_file() and p.name != "pacote.json"
    }
    for sobra in sorted(presentes - set(arquivos)):
        erro(f"arquivo '{sobra}' não está listado em 'arquivos'")

    lista: list[dict] = []
    total = 0
    for rel in arquivos:
        if not isinstance(rel, str) or not RE_CAMINHO.match(rel) or ".." in rel.split("/"):
            erro(f"caminho inválido: {rel!r}")
            continue
        p = pasta / rel
        if not p.is_file():
            erro(f"'{rel}' não existe")
            continue
        sufixo = "".join(Path(rel).suffixes[-1:]).lower()
        if sufixo not in EXTENSOES:
            erro(f"'{rel}': extensão não permitida (só código-fonte, texto e imagens)")
        dados = p.read_bytes()
        if dados.startswith(ASSINATURAS_BINARIAS):
            erro(f"'{rel}' parece um executável ou arquivo compactado")
        if len(dados) > MAX_ARQUIVO:
            erro(f"'{rel}' passa de {MAX_ARQUIVO // 1024} KiB")
        total += len(dados)
        lista.append({"caminho": rel, "tamanho": len(dados), "sha256": sha256(p)})
    if total > MAX_PACOTE:
        erro(f"o pacote passa de {MAX_PACOTE // (1 << 20)} MiB")

    entrada = dict(m)
    entrada["arquivos"] = lista
    return entrada, erros


def montar_indice() -> tuple[dict, list[str]]:
    erros: list[str] = []
    pacotes: list[dict] = []
    if PACOTES.is_dir():
        for pasta in sorted(p for p in PACOTES.iterdir() if p.is_dir()):
            entrada, e = validar_pacote(pasta)
            erros.extend(e)
            if entrada is not None and not e:
                pacotes.append(entrada)
    for p in PACOTES.iterdir() if PACOTES.is_dir() else []:
        if p.is_file():
            erros.append(f"pacotes/{p.name}: só pastas de pacote ficam em pacotes/")
    return {"versao_formato": VERSAO_FORMATO, "pacotes": pacotes}, erros


def serializar(indice: dict) -> str:
    return json.dumps(indice, ensure_ascii=False, indent=2) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"validar", "gerar"}:
        print((__doc__ or "").strip(), file=sys.stderr)
        return 2
    indice, erros = montar_indice()
    if erros:
        for e in erros:
            print(f"ERRO {e}", file=sys.stderr)
        return 1
    texto = serializar(indice)
    if argv[1] == "gerar":
        INDICE.write_text(texto, encoding="utf-8", newline="\n")
        print(f"index.json gerado com {len(indice['pacotes'])} pacote(s)")
        return 0
    atual = INDICE.read_text(encoding="utf-8") if INDICE.is_file() else ""
    if atual != texto:
        print(
            "ERRO index.json desatualizado: rode 'python ferramentas/loja.py gerar' e commite",
            file=sys.stderr,
        )
        return 1
    print(f"ok: {len(indice['pacotes'])} pacote(s) válidos e index.json em dia")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
