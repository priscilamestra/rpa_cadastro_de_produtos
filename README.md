## RPA — Cadastro de Produtos

Robô de automação de interface que elimina o trabalho manual de *data entry* em sistemas ERP legados.  
Lê uma planilha `.csv`, abre o navegador, faz login e cadastra cada produto automaticamente — campo por campo.

#![RPA em ação](img/rpa_cadastro_no_sistema.gif)

---

### Problema que resolve

Sistemas corporativos antigos frequentemente não possuem API ou importação em massa.  
Isso obriga funcionários a horas de "copiar e colar" para cadastrar produtos — lento, caro e sujeito a erro humano.

---

### Como funciona

1. Usuário deposita o `.csv` na pasta `Entrada/`
2. Executa o robô (`rpa-cadastro-de-produtos.exe`)
3. O robô abre o Chrome, faz login e cadastra todos os produtos automaticamente
4. Ao finalizar, move o `.csv` para `Processados/` — evitando duplicidade

---

### Interface

````
╭─────────────────────────────────────╮
│    Menu Principal                   │
│                                     │
│  RPA — Cadastro de Produtos         │
│                                     │
│   [1] Iniciar Cadastro              │
│   [2] Configurar Credenciais        │
│   [3] Sair                          │
╰─────────────────────────────────────╯
Escolha uma opção:
````

---

### Estrutura de entrega ao cliente

````
dist/
├── rpa-cadastro-de-produtos.exe   ← executável, clique duplo para iniciar
├── Entrada/                       ← deposite o .csv aqui antes de rodar
└── Processados/                   ← o robô move o .csv para cá após concluir
````

---

### Formato do CSV esperado

O arquivo `.csv` deve conter as seguintes colunas, nesta ordem:

| codigo | marca | tipo | categoria | preco_unitario | custo | obs |
|--------|-------|------|-----------|----------------|-------|-----|
| 001 | Marca X | Eletrônico | Informática | 299.90 | 180.00 | |
| 002 | Marca Y | Periférico | Acessórios | 89.90 | 45.00 | Frágil |

> A coluna `obs` é opcional — pode ficar vazia.

---

### Configuração (primeira execução)

Na primeira vez que o `.exe` rodar, o sistema pede automaticamente:

````
   Setup de Credenciais
   E-mail: usuario@empresa.com
   Senha:  ********
   URL do sistema (ex: http://erp.empresa.com):
   Credenciais salvas em config.json
````

As credenciais ficam salvas localmente em `config.json`.  
Para reconfigurar, basta escolher a opção `[2] Configurar Credenciais` no menu.

---

### Stack técnica

| Tecnologia | Função |
|---|---|
| `Python 3.x` | Linguagem base |
| `pyautogui` | Automação de teclado e mouse |
| `pandas` | Leitura e manipulação do CSV |
| `rich` | Interface de terminal com barra de progresso |
| `PyInstaller` | Empacotamento em `.exe` autossuficiente |
| `uv` | Gerenciamento de dependências |

---

### Arquitetura do código

````
rpa-cadastro-de-produtos/
│
├── main.py        → menu CLI, orquestra o fluxo
├── config.py      → leitura e escrita de credenciais (config.json)
├── automacao.py   → toda a interação com o navegador e o ERP
│
├── Entrada/       → input: CSVs aguardando processamento
└── Processados/   → output: CSVs já processados
````

Cada módulo tem responsabilidade única — manutenção cirúrgica, sem efeitos colaterais.

---

### Adaptação para outros sistemas

Para adaptar o robô a um ERP diferente, apenas um trecho precisa ser alterado:

**`automacao.py` → função `_preencher_linha()`**

```python
# Ajuste a lista de campos para bater com a ordem dos campos na tela do novo sistema
campos = ['codigo', 'marca', 'tipo', 'categoria', 'preco_unitario', 'custo']
```

`main.py` e `config.py` não precisam ser tocados.

---

### Rodando em desenvolvimento

```powershell
# Instala as dependências
uv sync

# Roda sem compilar o .exe
uv run python main.py
```

---

### Gerando o executável

```powershell
uv run pyinstaller --onefile --console --name "rpa-cadastro-de-produtos" main.py

# Após gerar, cria as pastas de entrega
mkdir dist/Entrada
mkdir dist/Processados
```

---

### Requisitos da máquina do cliente

- Windows 10 ou superior
- Google Chrome instalado
- Nenhuma instalação de Python necessária — o `.exe` é autossuficiente

---

### Licença

MIT
````