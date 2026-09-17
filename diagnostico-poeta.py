#!/usr/bin/env python3
"""
DIAGNÓSTICO do Poeta dos Commits.
Roda solto (NÃO é hook) e fala em voz alta o que está acontecendo.
Uso:
    python diagnostico-poeta.py
"""
import os, sys, subprocess

print("=" * 50)
print("1) Python em uso:", sys.executable)
print("   versão:", sys.version.split()[0])

# 2) biblioteca anthropic
try:
    import anthropic
    print("2) biblioteca anthropic: OK")
except ImportError:
    print("2) biblioteca anthropic: FALTANDO  -> pip install anthropic")
    sys.exit()

# 3) API key
key = os.environ.get("ANTHROPIC_API_KEY")
if key:
    print(f"3) ANTHROPIC_API_KEY: encontrada (começa com {key[:7]}...)")
else:
    print("3) ANTHROPIC_API_KEY: NÃO ENCONTRADA neste terminal")
    sys.exit()

# 4) diff staged
try:
    diff = subprocess.check_output(
        ["git", "diff", "--cached", "--no-color"],
        text=True, stderr=subprocess.DEVNULL
    )
except Exception as e:
    print("4) git diff falhou:", e)
    sys.exit()

if diff.strip():
    print(f"4) diff staged: OK ({len(diff)} caracteres)")
else:
    print("4) diff staged: VAZIO -> faça 'git add' antes. É por isso que sai calado.")
    sys.exit()

# 5) chamada à IA
print("5) chamando a IA...")
try:
    client = anthropic.Anthropic(api_key=key)
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content":
            "Escreva UMA mensagem de commit em Conventional Commits, "
            "em português, para este diff. Responda só a mensagem:\n\n" + diff[:12000]}],
    )
    msg = "".join(b.text for b in resp.content if b.type == "text").strip()
    print("=" * 50)
    print("MENSAGEM GERADA:\n")
    print(msg)
    print("=" * 50)
    print("\n>> Se você chegou aqui, TUDO funciona. O problema é só o Git")
    print("   não estar executando o hook. A gente conserta o hook agora.")
except Exception as e:
    print("5) A IA falhou:", repr(e))
