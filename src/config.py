# config.py
import json
import os
import sys
import hashlib

# BASE_DIR sempre relativo a onde o .exe (ou script) está rodando
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def config_existe() -> bool:
    """Retorna True se o config.json já foi criado."""
    return os.path.exists(CONFIG_PATH)


def carregar_config() -> dict:
    """Lê o config.json e retorna dicionário."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_config(email: str, senha: str, url: str):
    """
    Salva as credenciais preservando campos extras já existentes (ex: senha_acesso).
    Bug corrigido: antes sobrescrevia o arquivo inteiro, apagando a senha_acesso.
    """
    dados = carregar_config() if config_existe() else {}
    dados["email"] = email
    dados["senha"] = senha
    dados["url"]   = url  # URL salva como digitada, sem .lower() (URLs são case-sensitive)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)


def definir_senha_acesso(senha: str):
    """Salva a senha de acesso como hash SHA-256. Não afeta os outros campos."""
    dados = carregar_config() if config_existe() else {}
    dados["senha_acesso"] = hashlib.sha256(senha.encode()).hexdigest()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)


def verificar_acesso() -> bool:
    """
    Verifica se o usuário tem autorização para rodar o sistema.
    Retorna True se senha correta ou se não há senha configurada.
    Bug corrigido: contador mostrava número errado de tentativas restantes.
    """
    if not config_existe():
        return True  # primeira execução, sem senha ainda

    config = carregar_config()
    senha_armazenada = config.get("senha_acesso")

    if not senha_armazenada:
        return True  # sem senha configurada, libera acesso

    for tentativa in range(3):
        entrada = input(f"🔐 Senha de acesso ({3 - tentativa} tentativa(s) restante(s)): ").strip()
        if hashlib.sha256(entrada.encode()).hexdigest() == senha_armazenada:
            return True
        print("   Senha incorreta.")

    return False  # bloqueado após 3 tentativas

def verificar_senha_atual(senha: str) -> bool:
    """Compara a senha digitada com o hash armazenado."""
    config = carregar_config()
    return hashlib.sha256(senha.encode()).hexdigest() == config.get("senha_acesso", "")


def remover_senha_acesso():
    """Remove a senha de acesso do config.json, deixando o sistema sem proteção."""
    dados = carregar_config() if config_existe() else {}
    dados.pop("senha_acesso", None)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)

def setup_interativo():
    """Coleta e salva credenciais do sistema. Senha de acesso é gerenciada pelo menu."""
    print("\nSetup de Credenciais")
    email = input("   E-mail: ").strip()
    senha = input("   Senha:  ").strip()
    url   = input("   URL do sistema (ex: http://erp.empresa.com): ").strip()
    salvar_config(email, senha, url)
    print("✅  Credenciais salvas em config.json\n")