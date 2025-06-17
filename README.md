# ✅ Comparador Sistec-SIGAA

Este script cruza dados de alunos entre os sistemas **Sistec** e **SIGAA**, usando Python e arquivos CSV, com interface gráfica.

---

## ▶️ Como usar

1. **Instale o Python**

   * Baixe e instale o Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   * Na instalação, marque a opção **"Add Python to PATH"**.

2. **Execute o script**

   * Dê um duplo clique no arquivo `sigaa-sistec.py`, ou clique com o botão direito > "Abrir com..." > **Python**.

3. **Na interface gráfica:**

   * Clique em **"Selecionar arquivo SIGAA"** e escolha o CSV exportado do SIGAA.
   * Clique em **"Selecionar arquivo SISTEC"** e escolha o CSV exportado do SISTEC.
   * Depois, clique em **"Iniciar Processamento"**.

4. **O que acontece**

   * O script verifica se o `pandas` está instalado. Se não estiver, ele instala automaticamente.
   * Lê os arquivos selecionados.
   * Filtra apenas os alunos com situação **"EM\_CURSO"** no SISTEC.
   * Compara os CPFs com os do SIGAA.
   * Gera três arquivos CSV automaticamente:

     * `apenas_no_sistec.csv`
     * `apenas_no_sigaa.csv`
     * `diferencas_curso.csv`

---

## 📌 Requisitos

* Python 3.7 ou superior.
* Conexão com a internet (somente na primeira execução, para instalar o pandas automaticamente).

---

## 📂 Arquivos gerados

| Nome do arquivo        | Descrição                                                |
| ---------------------- | -------------------------------------------------------- |
| `apenas_no_sistec.csv` | Alunos presentes no SISTEC mas não encontrados no SIGAA. |
| `apenas_no_sigaa.csv`  | Alunos presentes no SIGAA mas não encontrados no SISTEC. |
| `diferencas_curso.csv` | Alunos presentes em ambos, mas com cursos diferentes.    |

---

## ⚠️ Possíveis erros

| Mensagem de erro                 | Causa                                            | Solução                                              |
| -------------------------------- | ------------------------------------------------ | ---------------------------------------------------- |
| `Arquivos CSV não selecionados.` | Você não escolheu os dois arquivos na interface. | Clique nos botões para selecionar ambos os arquivos. |
| `pandas` não é reconhecido       | Python não instalado corretamente.               | Reinstale o Python e marque "Add to PATH".           |

---

Feito com o intuito de facilitar a comparação de dados entre sistemas
