# Publicacao do pacote `msgram_core`

Guia de como empacotar e publicar este repositorio no PyPI. Escrito para os
proximos grupos: leia inteiro antes da primeira release.

Pacote no PyPI: **`msgram_core`** (instalado como `msgram-core`).

---

## TL;DR

A publicacao e automatica via GitHub Actions e **Trusted Publishing (OIDC)**:
nao existe token nem secret no repositorio. Tudo e disparado por **tag git**.

| Tag que voce cria        | Onde publica       | Quando usar                          |
|--------------------------|--------------------|--------------------------------------|
| `vX.Y.ZrcN` (`v1.5.4rc1`)| TestPyPI           | Testar o pacote antes de producao    |
| `vX.Y.Z` (`v1.5.4`)      | PyPI (producao)    | Release final, depois de validar a rc|

**Trava de seguranca:** a tag final (`vX.Y.Z`) so publica em producao se ja
existir uma release candidate (`vX.Y.ZrcN`) da mesma versao no TestPyPI. Sem rc,
o job falha. E impossivel publicar em producao sem ter testado antes.

---

## Fluxo completo de uma release (passo a passo)

1. **Bump da versao para a rc.** Em `pyproject.toml`, ajuste:
   ```toml
   version = "1.5.4rc1"
   ```
   A versao do `pyproject.toml` tem que bater EXATAMENTE com a tag, senao o CI
   falha de proposito (step "Validar tag == versao do pyproject").
2. **Commit + tag da rc:**
   ```bash
   git commit -am "chore: bump 1.5.4rc1"
   git tag v1.5.4rc1
   git push origin develop --tags
   ```
   O push da tag dispara o workflow, que publica no **TestPyPI**.
3. **Teste a rc** instalando do TestPyPI (secao abaixo). Rode o que precisar.
4. **Se estiver tudo certo, prepare a final.** No `pyproject.toml`:
   ```toml
   version = "1.5.4"
   ```
5. **Commit + tag final:**
   ```bash
   git commit -am "chore: release 1.5.4"
   git tag v1.5.4
   git push origin develop --tags
   ```
   O workflow roda o **gate** (confere que `1.5.4rcN` existe no TestPyPI) e, se
   passar, publica em **producao**.

Achou um problema na rc? Corrija, suba a versao da rc (`1.5.4rc2`) e repita do
passo 1. So promova para final quando a rc estiver boa.

---

## Pre-requisitos: configurar o Trusted Publisher (uma vez por projeto)

Quem tiver acesso de **owner** do projeto no PyPI precisa registrar o publisher
confiavel nos DOIS indices (sao contas/sites separados):

- Producao: <https://pypi.org/manage/project/msgram_core/settings/publishing/>
- Teste: <https://test.pypi.org/manage/project/msgram_core/settings/publishing/>

Em cada um, adicione um "GitHub" trusted publisher com:

| Campo               | Valor                              |
|---------------------|------------------------------------|
| Owner               | `fga-eps-mds`                      |
| Repository name     | `2026.1-MeasureSoftGram-Core`     |
| Workflow filename   | `python-publish.yml`              |
| Environment name    | `pypi` no PyPI / `testpypi` no TestPyPI |

Depois, no GitHub do repo (Settings > Environments), crie os environments
**`testpypi`** e **`pypi`**. Recomendado: no `pypi`, marque "Required reviewers"
com alguem do time, assim toda release de producao passa por um OK humano alem
do gate da rc.

> Nota: Trusted Publishing substitui os antigos secrets `PYPI_API_TOKEN` e
> `TEST_PYPI_API_TOKEN`. Eles nao sao mais usados e podem ser removidos.

---

## Como testar a partir do TestPyPI

O TestPyPI nao tem todas as dependencias pesadas (pandas, numpy, scipy,
scikit-learn). Por isso o `--extra-index-url` aponta para o PyPI de producao,
de onde essas deps sao baixadas:

```bash
uv venv --python 3.10 .venv
uv pip install --python .venv/bin/python \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  "msgram-core==1.5.4rc1"

.venv/bin/python -c "import core; print('import ok')"
```

(Com `pip` puro: `pip install --index-url ... --extra-index-url ... msgram-core==1.5.4rc1`.)

---

## Ordem de publicacao entre os pacotes do MeasureSoftGram

O ecossistema tem tres pacotes com dependencia entre eles:

```
msgram (CLI)  ->  depende de  ->  msgram-core  +  msgram-parser
```

`msgram_core` (este repo) **nao depende** dos outros, entao faz parte da
primeira onda. Ordem recomendada ao subir versoes novas em producao:

1. **msgram-core** e **msgram-parser** (este repo entra aqui)
2. so depois, **msgram** (CLI)

Motivo: quando o CLI for publicado, o PyPI precisa ja ter as versoes novas de
core e parser disponiveis para resolver as dependencias.

---

## Versionamento

- Segue [PEP 440](https://peps.python.org/pep-0440/). Release candidate e
  `X.Y.ZrcN` (ex: `1.5.4rc1`), final e `X.Y.Z`.
- Cada versao so pode ser publicada **uma vez** em cada indice. Para republicar,
  suba o numero (nao da para sobrescrever no PyPI nem no TestPyPI).
- A tag git sempre tem o prefixo `v` (`v1.5.4rc1`, `v1.5.4`).

---

## Troubleshooting

| Sintoma | Causa provavel / solucao |
|---|---|
| `403 ... isn't allowed to upload to project` | Trusted publisher nao configurado ou com campo divergente (owner/repo/workflow/environment). Confira a secao de pre-requisitos. |
| `400 File already exists` | Essa versao ja foi publicada nesse indice. Suba o numero da versao. |
| Job de producao falhou no "Gate" | Nao existe rc da mesma versao no TestPyPI. Publique e teste a `vX.Y.ZrcN` primeiro. |
| `Tag ... difere da versao em pyproject.toml` | A tag e a `version` do `pyproject.toml` precisam ser iguais. Ajuste e re-tague. |
| `pip` nao acha pandas/scipy ao instalar do TestPyPI | Faltou o `--extra-index-url https://pypi.org/simple/`. |

---

## Referencias

- Trusted Publishing (PyPI): <https://docs.pypi.org/trusted-publishers/>
- Action oficial: <https://github.com/pypa/gh-action-pypi-publish>
- Workflow deste repo: `.github/workflows/python-publish.yml`
