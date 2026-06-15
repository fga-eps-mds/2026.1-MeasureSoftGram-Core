# Publicacao do pacote `msgram_core`

Guia de como empacotar e publicar este repositorio no PyPI. Escrito para os
proximos grupos: leia inteiro antes da primeira release.

Pacote no PyPI: **`msgram_core`** (instalado como `msgram-core`).

---

## TL;DR

A publicacao e automatica via GitHub Actions e **Trusted Publishing (OIDC)**:
nao existe token nem secret no repositorio. Tudo acontece no **PyPI de producao**,
disparado por **tag git**. O "teste antes do final" e feito com **release
candidate (pre-release)**, que o `pip` normal ignora.

| Tag que voce cria         | O que publica                  | Quem instala                              |
|---------------------------|--------------------------------|-------------------------------------------|
| `vX.Y.ZrcN` (`v1.5.4rc1`) | pre-release no PyPI            | so quem pedir: `pip install --pre` ou `==1.5.4rc1` |
| `vX.Y.Z` (`v1.5.4`)       | versao final no PyPI          | todo mundo: `pip install msgram-core`     |

**Trava de seguranca:** a tag final (`vX.Y.Z`) so publica se ja existir uma
release candidate (`vX.Y.ZrcN`) da mesma versao no PyPI. Sem rc, o job falha. E
impossivel publicar a final sem ter testado a rc antes.

### Por que pre-release em vez de TestPyPI?

Pre-release na producao e o que numpy, pandas, Django, pip e o proprio CPython
fazem a cada release: a rc fica publicada, mas o `pip install` normal **nao a
pega** (PEP 440 ignora pre-releases por padrao). Quem quer testar pede de
proposito com `--pre`. O TestPyPI serve pra testar o *processo de publicacao*
(pipeline/build), nao pra distribuir software pra alguem usar, e e um sandbox
volatil. Por isso o ciclo de release vive na producao.

---

## Fluxo completo de uma release (passo a passo)

1. **Bump da versao para a rc.** Em `pyproject.toml`:
   ```toml
   version = "1.5.4rc1"
   ```
   A versao do `pyproject.toml` tem que bater EXATAMENTE com a tag, senao o CI
   falha de proposito (step "Validar tag == versao do pyproject").
2. **Commit + tag da rc:**
   ```bash
   git commit -am "chore: bump 1.5.4rc1"
   git tag v1.5.4rc1
   git push origin main --tags
   ```
   O push da tag dispara o workflow, que publica a rc como pre-release no PyPI.
3. **Teste a rc** (secao abaixo). Rode o que precisar.
4. **Se estiver tudo certo, prepare a final.** No `pyproject.toml`:
   ```toml
   version = "1.5.4"
   ```
5. **Commit + tag final:**
   ```bash
   git commit -am "chore: release 1.5.4"
   git tag v1.5.4
   git push origin main --tags
   ```
   O workflow roda o **gate** (confere que `1.5.4rcN` existe no PyPI) e, se
   passar, publica a versao final.

Achou um problema na rc? Corrija, suba a versao da rc (`1.5.4rc2`) e repita do
passo 1. So promova para final quando a rc estiver boa.

> **Deu ruim numa rc ja publicada?** Use **yank** na pagina do projeto
> (Manage > Releases > Options > Yank): a versao para de ser instalada (o `pip`
> ignora), sem afetar quem ja tinha pinado. Evite **deletar**, porque o numero
> da versao fica queimado (nao da pra reusar).

---

## Pre-requisitos: configurar o Trusted Publisher (uma vez por projeto)

> Onde este workflow roda de verdade: a producao sai do repositorio que e dono
> do projeto no PyPI. No fluxo da FGA, o trabalho do semestre acontece no fork
> (`2026.1-...`) e e integrado por merge no repositorio upstream
> (`MeasureSoftGram-Core`), de onde a release sai. Configure o trusted publisher
> apontando para o repositorio de onde a tag de release sera criada.

Quem tiver acesso de **owner** do projeto no PyPI registra o publisher confiavel
em <https://pypi.org/manage/project/msgram_core/settings/publishing/>, aba
GitHub:

| Campo               | Valor                                          |
|---------------------|------------------------------------------------|
| Owner               | `fga-eps-mds`                                  |
| Repository name     | repo de onde sai a release (ex: `MeasureSoftGram-Core`) |
| Workflow filename   | `python-publish.yml`                          |
| Environment name    | `pypi`                                         |

E crie o environment **`pypi`** nesse repo (GitHub > Settings > Environments).
Opcional mas recomendado: marque "Required reviewers" no `pypi` pra exigir um OK
humano antes de cada publicacao.

> Trusted Publishing substitui os antigos secrets `PYPI_API_TOKEN` e
> `TEST_PYPI_API_TOKEN`. Eles nao sao mais usados e podem ser removidos.

---

## Como testar a rc

```bash
uv venv --python 3.10 .venv
uv pip install --python .venv/bin/python --prerelease=allow "msgram-core==1.5.4rc1"
.venv/bin/python -c "import core; print('import ok')"
```

(Com `pip` puro: `pip install --pre "msgram-core==1.5.4rc1"`.)

Repare que aqui nao precisa de `--extra-index-url`: tudo vem do PyPI de producao,
inclusive as dependencias pesadas (pandas, numpy, scipy, scikit-learn).

---

## Ordem de publicacao entre os pacotes do MeasureSoftGram

```
msgram (CLI)  ->  depende de  ->  msgram-core  +  msgram-parser
```

`msgram_core` (este repo) **nao depende** dos outros, entao faz parte da primeira
onda. Ordem ao subir versoes novas:

1. **msgram-core** e **msgram-parser** (este repo entra aqui)
2. so depois, **msgram** (CLI)

Motivo: quando o CLI for publicado, o PyPI precisa ja ter as versoes novas de
core e parser disponiveis para resolver as dependencias.

---

## Versionamento

- Segue [PEP 440](https://peps.python.org/pep-0440/). Release candidate e
  `X.Y.ZrcN` (ex: `1.5.4rc1`), final e `X.Y.Z`.
- Cada versao so pode ser publicada **uma vez**. Para republicar, suba o numero
  (nao da para sobrescrever no PyPI).
- A tag git sempre tem o prefixo `v` (`v1.5.4rc1`, `v1.5.4`).

---

## Troubleshooting

| Sintoma | Causa provavel / solucao |
|---|---|
| `403 ... isn't allowed to upload to project` | Trusted publisher nao configurado ou com campo divergente (owner/repo/workflow/environment). Confira os pre-requisitos. |
| `400 File already exists` | Essa versao ja foi publicada. Suba o numero da versao. |
| Job da versao final falhou no "Gate" | Nao existe rc da mesma versao no PyPI. Publique e teste a `vX.Y.ZrcN` primeiro. |
| `Tag ... difere da versao em pyproject.toml` | A tag e a `version` do `pyproject.toml` precisam ser iguais. Ajuste e re-tague. |
| `pip install` nao acha a rc | Pre-release nao vem por padrao. Use `--pre` ou pin exato (`==1.5.4rc1`). |

---

## TestPyPI (opcional, so para testar o pipeline)

Se um dia precisar testar mudancas no proprio processo de publicacao sem mexer na
producao, da pra usar o TestPyPI manualmente. Atencao: os nomes oficiais no
TestPyPI estao presos numa conta antiga sem acesso, entao la so da pra publicar
com nomes sufixados (ex: `msgram-core-test`). Nao faz parte do fluxo de release.

---

## Referencias

- Trusted Publishing (PyPI): <https://docs.pypi.org/trusted-publishers/>
- Pre-releases (PEP 440): <https://peps.python.org/pep-0440/#pre-releases>
- Action oficial: <https://github.com/pypa/gh-action-pypi-publish>
- Workflow deste repo: `.github/workflows/python-publish.yml`
