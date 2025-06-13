# ✅ Comparador Sistec-SIGAA

Este script cruza dados de alunos entre os sistemas **Sistec** e **SIGAA**, via python e arquivos CSV.

---

## 📁 Estrutura esperada de pastas

Coloque todos os arquivos da seguinte forma:

```
[Pasta onde está o script]
├── sigaa-sistec.py 
└── CSVs 
    ├── sistec.csv 
    └── sigaa.csv 
```

---

> **Importante:** Os arquivos `.csv` devem estar exatamente com os nomes:  
> `sistec.csv` e `sigaa.csv`, dentro da pasta `CSVs`.

---

## ▶️ Como usar

1. **Instale o Python**
   - Baixe e instale o Python: https://www.python.org/downloads/
   - Na instalação, marque a opção **"Add Python to PATH"**.

2. **Prepare os arquivos**
   - Dentro da pasta CSVs coloque os arquivos:
     - `sistec.csv` (exportado do Sistec)
     - `sigaa.csv` (exportado do SIGAA)

3. **Execute o script**
   - Dê um duplo clique no arquivo `sigaa-sistec.py`
   - Ou clique com o botão direito > "Abrir com..." > **Python**]
   - Na tela do app aperte no botão Iniciar Processamento e espere a saida

4. **O que acontece**
   - O script verifica se o `pandas` está instalado. Se não estiver, ele instala automaticamente.
   - Depois, ele lê os arquivos, filtra os alunos "EM_CURSO" do Sistec, e cruza os CPFs com os do SIGAA.
   - Por fim, ele gera os novos arquivos

---

## 📌 Requisitos

- Python 3.7 ou superior.
- Conexão com a internet (somente na primeira execução, para instalar o pandas).

---

## ⚠️ Possíveis erros

| Mensagem de erro                              | Causa                                                | Solução                                                       |
|-----------------------------------------------|-------------------------------------------------------|----------------------------------------------------------------|
| `Arquivo 'CSVs/sistec.csv' não encontrado`    | O arquivo `sistec.csv` não está na pasta `CSVs`.     | Verifique se colocou o arquivo no lugar certo e com o nome correto. |
| `pandas` não é reconhecido                    | O Python não está instalado corretamente ou o script foi aberto sem ele. | Reinstale o Python e marque "Add to PATH" na instalação.         |

---

