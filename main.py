# main.py

import os
import glob
import sys
from rich.console import Console
from rich.panel import Panel
from config import config_existe, carregar_config, setup_interativo, verificar_acesso
from automacao import executar_cadastro, carregar_progresso, limpar_progresso

console = Console()

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(BASE_DIR, "Entrada")


def listar_csvs() -> list[str]:
    """Cria a pasta Entrada/ se não existir e retorna todos os .csv dentro dela."""
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    return glob.glob(os.path.join(PASTA_ENTRADA, "*.csv"))


def menu():
    """Loop principal do terminal."""
    while True:
        console.print(Panel.fit(
            "[bold cyan]RPA — Cadastro de Produtos[/bold cyan]\n\n"
            " [1] Iniciar Cadastro\n"
            " [2] Configurar Credenciais\n"
            " [3] Sair",
            title="Menu Principal"
        ))

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            _iniciar_cadastro()
        elif opcao == "2":
            setup_interativo()
        elif opcao == "3":
            console.print("[yellow]Até logo![/yellow]")
            break
        else:
            console.print("[red]Opção inválida. Tente novamente.[/red]")


def _iniciar_cadastro():
    """Orquestra o fluxo completo, incluindo retomada de progresso interrompido."""
    # Senha pedida aqui: protege a automação, não o menu inteiro
    if not verificar_acesso():
        console.print("[bold red]Acesso negado. Voltando ao menu.[/bold red]")
        return  # volta pro menu, não encerra o programa

    if not config_existe():
        console.print("[yellow]Nenhuma credencial encontrada. Vamos configurar agora.[/yellow]")
        setup_interativo()

    config = carregar_config()

    # ---------- VERIFICA CHECKPOINT ----------
    progresso = carregar_progresso()
    linha_inicio = 0

    if progresso:
        console.print("\n[yellow]⚠️  Execução anterior interrompida![/yellow]")
        console.print(f"   Arquivo  : [cyan]{progresso['arquivo']}[/cyan]")
        console.print(f"   Progresso: {progresso['ultima_linha_processada']} de {progresso['total']} produtos")
        console.print(f"   Data     : {progresso['timestamp']}\n")
        console.print(" [1] Continuar de onde parou")
        console.print(" [2] Recomeçar do início")
        console.print(" [3] Cancelar\n")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            linha_inicio = progresso['ultima_linha_processada']
            console.print(f"[green]Retomando a partir do produto {linha_inicio + 1}...[/green]\n")
        elif escolha == "2":
            limpar_progresso()
            linha_inicio = 0
            console.print("[green]Recomeçando do início...[/green]\n")
        else:
            return  # volta pro menu principal

    # ---------- BUSCA CSVs ----------
    csvs = listar_csvs()

    if not csvs:
        console.print("[red]Nenhum .csv encontrado em Entrada/. Deposite o arquivo e tente novamente.[/red]")
        return

    console.print(f"\n[green]{len(csvs)} arquivo(s) encontrado(s):[/green]")
    for i, caminho in enumerate(csvs, 1):
        console.print(f"  [{i}] {os.path.basename(caminho)}")

    # ---------- PROCESSA CADA CSV ----------
    for caminho in csvs:
        console.print(f"\n▶  Processando: [bold]{os.path.basename(caminho)}[/bold]")
        sucesso = executar_cadastro(config, caminho, linha_inicio)

        if sucesso:
            console.print("[green]✔  Concluído com sucesso.[/green]")
        else:
            console.print("[red]✘  Interrompido. O progresso foi salvo — rode novamente para continuar.[/red]")

        linha_inicio = 0  # reseta para o próximo CSV, se houver mais de um


if __name__ == "__main__":
    if not config_existe():
        console.print("[bold yellow]Primeira execução detectada! Vamos configurar suas credenciais.[/bold yellow]")
        setup_interativo()
    menu()