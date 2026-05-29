# config.py
# Módulo responsável por tudo que envolve credenciais:
# ler, salvar e coletar do usuário via terminal.
# Nenhuma outra parte do projeto lida com config.json — só este arquivo.

import json
import os
import sys

# Caminho absoluto do config.json, sempre na mesma pasta do .exe
# os.path.abspath(__file__) → caminho completo deste arquivo
# os.path.dirname(...)      → pasta onde ele está
# os.path.join(...)         → cola o nome do arquivo no final

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def config_existe() -> bool:
    """Retorna True se o config.json já foi criado, False se é a primeira execução."""
    return os.path.exists(CONFIG_PATH)


def salvar_config(email: str, senha: str, url: str):
    """
    Recebe as três credenciais e salva no config.json com indentação legível.
    Sobrescreve o arquivo se já existir — usado tanto no setup inicial
    quanto na opção [2] Configurar Credenciais do menu.
    """
    dados = {"email": email, "senha": senha, "url": url}

    # "w" cria o arquivo se não existir, ou sobrescreve se já existir
    # encoding="utf-8" garante suporte a caracteres especiais no caminho/senha
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)  # indent=2 deixa o JSON legível se alguém abrir o arquivo


def carregar_config() -> dict:
    """
    Lê o config.json e retorna um dicionário pronto para uso.
    Chamada pelo main.py antes de iniciar a automação.

    Retorna: {"email": "...", "senha": "...", "url": "..."}
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)  # json.load converte o arquivo direto para dicionário Python


def setup_interativo():
    """
    Coleta as credenciais do usuário via terminal e salva no config.json.
    Chamada automaticamente na primeira execução e manualmente via opção [2] do menu.
    .strip() em cada input remove espaços acidentais que o usuário possa digitar.
    """
    print("\n🔧  Setup de Credenciais")
    email = input("   E-mail: ").strip()
    senha = input("   Senha:  ").strip()
    url   = input("   URL do sistema (ex: http://erp.empresa.com): ").strip()

    salvar_config(email, senha, url)  # Persiste tudo no disco

    print("✅  Credenciais salvas em config.json\n")