# automacao.py
import pandas as pd
import pyautogui
import shutil
import os
import subprocess
import winreg
import sys
import json
from datetime import datetime
from time import sleep
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.console import Console

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_PROCESSADOS = os.path.join(BASE_DIR, "Processados")
PROGRESSO_PATH    = os.path.join(BASE_DIR, "Processados", "progresso.json")


def salvar_progresso(nome_arquivo: str, ultima_linha: int, total: int):
    """Salva o ponto de parada após cada produto cadastrado."""
    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)
    dados = {
        "arquivo": nome_arquivo,
        "ultima_linha_processada": ultima_linha,
        "total": total,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    with open(PROGRESSO_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)


def carregar_progresso() -> dict | None:
    """Retorna o dicionário do progresso.json se existir, None caso contrário."""
    if os.path.exists(PROGRESSO_PATH):
        with open(PROGRESSO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def limpar_progresso():
    """Remove o progresso.json após conclusão bem-sucedida."""
    if os.path.exists(PROGRESSO_PATH):
        os.remove(PROGRESSO_PATH)

def _obter_caminho_chrome() -> str:
    """Busca o caminho real do chrome.exe no registro do Windows.
    Garante que --start-maximized funcione independente de como o Chrome foi instalado."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
        )
        path = winreg.QueryValue(key, None)
        winreg.CloseKey(key)
        return path
    except Exception:
        fallbacks = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]
        for path in fallbacks:
            if os.path.exists(path):
                return path
        return 'chrome'  # fallback genérico — espera que esteja no PATH do sistema

def executar_cadastro(config: dict, caminho_csv: str, linha_inicio: int = 0):   
    """
    Função principal da automação.
    linha_inicio → permite retomar de onde parou (default 0 = começo)
    Retorna True se concluiu, False se deu erro ou foi interrompido.
    """
    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

    try:
        tabela = pd.read_csv(caminho_csv)
    except Exception as e:
        print(f"[ERRO] Não consegui ler o CSV: {e}")
        return False

    nome_arquivo = os.path.basename(caminho_csv)
    total = len(tabela)

    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True

    # ---------- ABERTURA DO NAVEGADOR ----------
    chrome = _obter_caminho_chrome()
    # --new-window: força nova janela mesmo se Chrome já estiver aberto
    # garante que --start-maximized seja respeitado (Chrome ignora a flag se já estiver rodando)
    # sem shell=True: funciona igual em CMD e PowerShell (resolve o bug do 0.0.0.2)
    subprocess.Popen([
        chrome,
        '--incognito',
        '--new-window',
        '--start-maximized',
        config["url"]
    ])
    sleep(3)
    pyautogui.hotkey('win', 'up')  # segunda garantia: maximiza a janela ativa
    sleep(1)

    # ---------- LOGIN ----------
    pyautogui.press('tab')
    pyautogui.write(config["email"])
    pyautogui.press('tab')
    pyautogui.write(config["senha"])
    pyautogui.press('tab')
    pyautogui.press('enter')
    sleep(2)

    # ---------- POSICIONA NO PRIMEIRO CAMPO ----------
    pyautogui.hotkey('ctrl', 'l')
    sleep(1)
    pyautogui.press('esc')
    pyautogui.press('esc')
    sleep(1)
    pyautogui.press('tab')

    # ---------- LOOP COM BARRA DE PROGRESSO ----------
    linha = linha_inicio  # garante que o except consegue reportar mesmo se o loop não iniciar
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=Console(force_terminal=True),
        ) as progress:

            # completed=linha_inicio faz a barra começar já no ponto certo ao retomar
            task = progress.add_task("Cadastrando produtos...", total=total, completed=linha_inicio)

            for linha in tabela.index[linha_inicio:]:  # pula os já processados
                codigo = str(tabela.loc[linha, 'codigo'])
                marca  = str(tabela.loc[linha, 'marca'])
                progress.console.print(f"  → Produto {linha + 1}/{total}: [cyan]{codigo}[/cyan] | {marca}")
                _preencher_linha(tabela, linha)
                salvar_progresso(nome_arquivo, linha + 1, total)  # salva checkpoint após cada produto
                progress.advance(task)

    except pyautogui.FailSafeException:
        print("\n[INTERROMPIDO] Automação pausada pelo usuário.")
        return False
    except Exception as e:
        print(f"[ERRO] Travou no produto #{linha}: {e}")
        return False

    # ---------- PREVENÇÃO DE DUPLICIDADE ----------
    # Só chega aqui se o loop terminou sem exceção
    destino = os.path.join(PASTA_PROCESSADOS, nome_arquivo)
    shutil.move(caminho_csv, destino)
    limpar_progresso()  # tarefa concluída — apaga o checkpoint
    print(f"\n✅  Arquivo movido para Processados/{nome_arquivo}")
    return True


def _preencher_linha(tabela, linha):
    """Preenche todos os campos de UM produto no formulário."""
    campos = ['codigo', 'marca', 'tipo', 'categoria', 'preco_unitario', 'custo']
    for campo in campos:
        valor = str(tabela.loc[linha, campo])
        pyautogui.write(valor)
        pyautogui.press('tab')

    obs = str(tabela.loc[linha, 'obs'])
    if obs != 'nan':
        pyautogui.write(obs)
    pyautogui.press('tab')
    pyautogui.press('enter')