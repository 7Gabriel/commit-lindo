# Poeta dos Commits 🖋️

Git hook que lê o *diff* do que você está commitando e escreve a mensagem de
commit sozinho, no padrão **Conventional Commits**, usando a API da Anthropic.

Você digita `git commit` → o editor abre **já com a mensagem pronta**.

---

## Pré-requisitos

- **Python 3** (testado com 3.12)
- **Git**
- Uma **API key da Anthropic** válida — começa com `sk-ant-` (pegue em
  [console.anthropic.com](https://console.anthropic.com) → *API Keys*)
- Conta Anthropic com **créditos/billing ativo** (é pré-pago)

---

## Instalação (Windows) — passo a passo testado

> ⚠️ **Não use o Python da Microsoft Store.** Ele instala pacotes num lugar
> que ele mesmo não enxerga, e o hook vai falhar em silêncio. Use um
> **ambiente virtual (venv)**, como abaixo.

### 1. Crie e ative um venv dentro do repositório
```bash
python -m venv .venv
```
Ative conforme o seu terminal:
```bash
# Git Bash
source .venv/Scripts/activate
# PowerShell
.venv\Scripts\Activate.ps1
# CMD
.venv\Scripts\activate.bat
```
Deu certo quando aparece `(.venv)` no início da linha.

### 2. Instale a biblioteca no venv
```bash
python -m pip install anthropic
```

### 3. Descubra o caminho do Python do venv
```bash
python -c "import sys; print(sys.executable)"
```
Exemplo de saída: `D:\commit-lindo\.venv\Scripts\python.exe`
Esse caminho vai na **primeira linha do hook** (veja passo 4).

### 4. Instale o hook
Copie o arquivo `prepare-commit-msg` para dentro de:
```
<seu-repo>/.git/hooks/prepare-commit-msg
```
- O nome tem que ser **exatamente** `prepare-commit-msg` — **sem** `.py`, sem `.txt`, sem nada.
- A **primeira linha** do arquivo deve apontar para o Python do venv (o caminho do passo 3), assim:
  ```
  #!D:/commit-lindo/.venv/Scripts/python.exe
  ```
  > Isso faz o Git usar o Python certo (o que tem a lib), sem depender de PATH.

### 5. Configure a API key na sessão do terminal
```bash
# Git Bash
export ANTHROPIC_API_KEY="sk-ant-...sua-chave..."
# PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-...sua-chave..."
```
> Cole a chave inteira, sem espaços e sem quebrar a linha.

---

## Uso

```bash
git add .
git commit          # sem -m
```
O editor abre com a mensagem gerada pela IA no topo. Salve e feche para
confirmar (`:wq` no Vim).

> Com `git commit -m "..."` o hook **não** age de propósito — precisa ser
> `git commit` sem o `-m`.

---

## Diagnóstico (quando não funciona)

Rode o script `diagnostico-poeta.py`, que fala em voz alta onde está travando.
**Faça `git add` antes**, senão ele para no passo 4 (diff vazio):
```bash
echo "print('teste')" >> app.py
git add app.py
python diagnostico-poeta.py
```
Ele checa, em ordem: Python em uso → biblioteca → API key → diff → chamada à IA.

---

## Erros comuns (e a solução)

| Sintoma | Causa | Solução |
|---|---|---|
| Editor abre **sem** a mensagem da IA | O hook não rodou | Confira o nome exato do arquivo (`prepare-commit-msg`, sem extensão) e a 1ª linha apontando pro Python do venv |
| `biblioteca anthropic: FALTANDO` mesmo após instalar | Instalou no Python da Store, não no venv | Crie o venv, ative, e `python -m pip install anthropic` dentro dele |
| `Can not perform a '--user' install` | Há um venv ativo | Instale **sem** o `--user`: `python -m pip install anthropic` |
| `401 - invalid x-api-key` | Chave inválida/errada | Gere uma nova em console.anthropic.com; ela começa com `sk-ant-`. Confira também se há créditos |
| Roda solto mas falha no `git commit` | O Git não acha a lib ou a chave | 1ª linha do hook apontando pro Python do venv + `export` da chave na mesma sessão do commit |
| `python3` não encontrado (Windows) | Windows usa `python`, não `python3` | Não é problema: a 1ª linha do hook já aponta pro `.exe` direto |

---

## Segurança (importante para gravar vídeo)

- **Nunca** deixe a `ANTHROPIC_API_KEY` aparecer na tela. Faça o `export`/`$env:`
  com o terminal fora do quadro, ou limpe a tela (`clear` / `cls`) depois.
- Se uma chave já apareceu em qualquer lugar (tela, conversa, print),
  **revogue-a** no console e gere outra.
- Não commite a chave nem o `.venv/` — adicione ao `.gitignore`:
  ```
  .venv/
  .env
  ```

---

## Como funciona (resumo)

1. Antes de cada commit, o Git chama `prepare-commit-msg`.
2. O script pega o `git diff --cached` (o que está no stage).
3. Manda o diff para a API da Anthropic (`claude-sonnet-4-6`) pedindo uma
   mensagem em Conventional Commits.
4. Escreve a resposta no topo do arquivo de mensagem do commit.
5. Se algo falhar (sem chave, sem diff, sem internet), ele sai em silêncio e
   o commit segue normal — nada quebra.

---

*Parte do arsenal do canal **O Matuto Programador**.*
