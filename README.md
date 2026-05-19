## Automação RPA de Cadastro ERP com Servidor Integrado

Este projeto é uma automação de Processos Robóticos (RPA) desenvolvida em Python para simular o fluxo de trabalho em um sistema ERP. O diferencial desta solução é a capacidade de gerenciar seu próprio ambiente de execução, iniciando e finalizando o servidor web automaticamente.
![Tela de login do sistema ERP](img/login_sistema.png)
![Tela do formulário do sistema ERP](img/formulario_cadastro_produtos.png)
![Automação preenchendo os dados no formulário de cadastro de produtos](img/rpa_cadastro_no_sistema.gif)

## Requisitos de Sistema
- **Sistema Operacional:** Desenvolvido e testado exclusivamente para **Windows**. 
- **Motivo:** A automação utiliza atalhos de teclado (`Win + R`, `Ctrl + L`) e comandos de terminal (`python -m http.server`) específicos do ambiente Windows para garantir a execução fluida. Para usar em outros sistemas, mude os atalhos no próprio script.

## Diferenciais do Projeto

- **Servidor Auto-Gerenciado:** O script utiliza a biblioteca `subprocess` para iniciar um servidor HTTP local na porta 8000, eliminando a necessidade de configuração manual do ambiente de teste.

![Terminal iniciando o servidor HTTP local automaticamente](img/servidor_iniciando_terminal.png)
- **Arquitetura Resiliente (Try/Finally):** Implementação de blocos de tratamento que garantem o encerramento seguro de processos e a liberação de portas de rede, mesmo em caso de erro crítico na automação.
- **Navegação Dinâmica:** O robô utiliza atalhos de sistema (`Ctrl + L`, `TAB`) em vez de coordenadas fixas, garantindo compatibilidade com diferentes resoluções de monitor.

## Tecnologias Utilizadas

- **Python 3.14**
- **PyAutoGUI:** Automação de interface (teclado e mouse).
- **Pandas:** Manipulação da base de dados (CSV).
- **Subprocess & OS:** Gerenciamento de infraestrutura e caminhos de sistema.
- **HTML/CSS:** Sistema ERP para testes.

## Como Executar

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/rpa_cadastro_no_sistema.git](https://github.com/seu-usuario/rpa_cadastro_no_sistema.git)
cd rpa_cadastro_no_sistema

## ⚙️ Personalização (Coordenadas Fixas)

Caso você prefira utilizar coordenadas específicas para cliques na sua tela em vez da navegação por atalhos (`Ctrl + L`), o projeto inclui um script auxiliar de reserva:

### Script `posicao.py`
Este script serve para identificar as coordenadas exatas (X e Y) de qualquer campo ou da barra de URL no seu monitor.

**Como usar:**
1. Execute o script: `python posicao.py`
2. Posicione o mouse sobre o campo desejado (ex: barra de endereços ou campo de login).
3. Aguarde o tempo configurado (geralmente 5 segundos) e o script imprimirá as coordenadas no terminal.
4. Substitua os comandos de `hotkey` ou `press` relacionados a clicar nos campos no `main.py` por `pyautogui.click(x=VALOR, y=VALOR)` usando os números obtidos.
