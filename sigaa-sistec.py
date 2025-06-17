import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk, filedialog


import subprocess

def install_pandas():
    try:
        import pandas as pd
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        
install_pandas()
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

PASTA_ARQUIVOS = 'CSVs'
ARQ_SISTEC = os.path.join(PASTA_ARQUIVOS, 'sistec.csv')
ARQ_SIGAA = os.path.join(PASTA_ARQUIVOS, 'sigaa.csv')
ARQ_SAIDA_SISTEC = os.path.join(PASTA_ARQUIVOS, 'apenas_no_sistec.csv')
ARQ_SAIDA_SIGAA = os.path.join(PASTA_ARQUIVOS, 'apenas_no_sigaa.csv')
ARQ_DIFERENCAS_CURSO = os.path.join(PASTA_ARQUIVOS, 'diferencas_curso.csv')

def CPF_to_int(cpf):
    try:
        return int(str(cpf).replace('.', '').replace('-', '').split('.')[0])
    except Exception:
        return None

def filter(df, col, col_n, filtro):
    return df[df[col[col_n]].astype(str).str.contains(filtro, na=False)]

def ToList(df):
    return [dict(row) for _, row in df.iterrows()]

def find_differences_with_course_check(sistec, sigaa):
    cpfs_sistec_map = {CPF_to_int(s['NU_CPF']): s for s in sistec if CPF_to_int(s['NU_CPF']) is not None}
    cpfs_sigaa_map = {CPF_to_int(sg['CPF']): sg for sg in sigaa if CPF_to_int(sg['CPF']) is not None}

    cpfs_sistec_set = set(cpfs_sistec_map.keys())
    cpfs_sigaa_set = set(cpfs_sigaa_map.keys())

    diff_sistec_only = cpfs_sistec_set - cpfs_sigaa_set
    diff_sigaa_only = cpfs_sigaa_set - cpfs_sistec_set
    cpfs_in_common = cpfs_sistec_set.intersection(cpfs_sigaa_set)

    apenas_sistec = [{
        'CPF': cpfs_sistec_map[cpf]['NU_CPF'],
        'Nome': cpfs_sistec_map[cpf]['NO_ALUNO'],
        'Curso': cpfs_sistec_map[cpf].get('NO_CICLO_MATRICULA', ''),
        'Origem': 'SISTEC'
    } for cpf in diff_sistec_only]

    apenas_sigaa = [{
        'CPF': cpfs_sigaa_map[cpf]['CPF'],
        'Nome': cpfs_sigaa_map[cpf].get('Nome', ''),
        'Curso': cpfs_sigaa_map[cpf].get('Curso', ''),
        'Origem': 'SIGAA'
    } for cpf in diff_sigaa_only]

    diferencas_curso = []
    for cpf in cpfs_in_common:
        sistec_record = cpfs_sistec_map[cpf]
        sigaa_record = cpfs_sigaa_map[cpf]

        curso_sistec = sistec_record.get('NO_CICLO_MATRICULA', '').split('-')[0].strip().upper()
        curso_sigaa = sigaa_record.get('Curso', '').strip().upper()

        if curso_sistec != curso_sigaa:
            diferencas_curso.append({
                'CPF': sistec_record['NU_CPF'],
                'Nome_SISTEC': sistec_record['NO_ALUNO'],
                'Curso_SISTEC': sistec_record.get('NO_CICLO_MATRICULA', ''),
                'Nome_SIGAA': sigaa_record.get('Nome', ''),
                'Curso_SIGAA': sigaa_record.get('Curso', ''),
                'Tipo_Diferenca': 'Cursos_Diferentes'
            })

    return apenas_sistec, apenas_sigaa, diferencas_curso

def makeCSV(data, filename):
    df = pd.DataFrame(data) if data else pd.DataFrame()
    df.to_csv(filename, index=False, encoding='utf-8')

def update_progress(valor):
    progress_bar['value'] = valor
    root.update_idletasks()

def iniciar_processamento():
    try:
        os.makedirs(PASTA_ARQUIVOS, exist_ok=True)
        update_progress(5)

        if not os.path.exists(ARQ_SISTEC) or not os.path.exists(ARQ_SIGAA):
            messagebox.showerror("Erro", "Arquivos CSV não selecionados.")
            update_progress(0)
            return

        df_sistec = pd.read_csv(ARQ_SISTEC, sep=',')
        df_sigaa = pd.read_csv(ARQ_SIGAA, sep=',')
        update_progress(20)

        col_sistec = df_sistec.columns.tolist()
        sistec_filtrado = filter(df_sistec, col_sistec, 23, 'EM_CURSO')  # ajuste o índice conforme necessário
        sigaa_filtrado = df_sigaa
        update_progress(40)

        lista_sistec = ToList(sistec_filtrado)
        lista_sigaa = ToList(sigaa_filtrado)
        update_progress(50)

        apenas_sistec, apenas_sigaa, diferencas_curso = find_differences_with_course_check(lista_sistec, lista_sigaa)
        update_progress(70)

        makeCSV(apenas_sistec, ARQ_SAIDA_SISTEC)
        makeCSV(apenas_sigaa, ARQ_SAIDA_SIGAA)
        makeCSV(diferencas_curso, ARQ_DIFERENCAS_CURSO)
        update_progress(100)

        messagebox.showinfo("Concluído", f"""
✅ Arquivos gerados:
👥 Apenas no SISTEC: {len(apenas_sistec)}
👥 Apenas no SIGAA: {len(apenas_sigaa)}
📚 Diferenças de curso: {len(diferencas_curso)}
""")
        update_progress(0)
    except Exception as e:
        update_progress(0)
        messagebox.showerror("Erro", str(e))

# Interface gráfica
def start_interface():
    global root, progress_bar, ARQ_SISTEC, ARQ_SIGAA
    global label_sigaa, label_sistec

    root = tk.Tk()
    root.title("🔍 Comparador SIGAA x SISTEC")
    root.geometry("500x420")
    root.configure(bg="#f9f9f9")

    fonte_titulo = ("Segoe UI", 12, "bold")
    fonte_padrao = ("Segoe UI", 10)

    espaco = 8

    tk.Label(root, text="Selecione os arquivos CSV:", font=fonte_titulo, bg="#f9f9f9").pack(pady=(15, espaco))

    btn_sigaa = tk.Button(root, text="📂 Selecionar arquivo SIGAA", font=fonte_padrao, bg="#e0f7fa", relief="groove", bd=2, command=select_sigaa)
    btn_sigaa.pack(pady=(0, 3))
    label_sigaa = tk.Label(root, text="Nenhum arquivo selecionado", font=("Segoe UI", 9), fg="gray", bg="#f9f9f9")
    label_sigaa.pack(pady=(0, espaco))

    btn_sistec = tk.Button(root, text="📂 Selecionar arquivo SISTEC", font=fonte_padrao, bg="#e0f7fa", relief="groove", bd=2, command=select_sistec)
    btn_sistec.pack(pady=(0, 3))
    label_sistec = tk.Label(root, text="Nenhum arquivo selecionado", font=("Segoe UI", 9), fg="gray", bg="#f9f9f9")
    label_sistec.pack(pady=(0, espaco))

    tk.Label(root, text="Depois de selecionar os arquivos:", font=fonte_titulo, bg="#f9f9f9").pack(pady=(10, espaco))

    btn_processar = tk.Button(root, text="✅ Iniciar Processamento", font=fonte_padrao, bg="#4caf50", fg="white", relief="raised", bd=3, command=iniciar_processamento)
    btn_processar.pack(pady=(0, espaco + 5))

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
    progress_bar.pack(pady=(0, espaco + 10))

    btn_sair = tk.Button(root, text="❌ Sair", font=fonte_padrao, bg="#ff5252", fg="white", relief="flat", command=root.destroy)
    btn_sair.pack(pady=(0, 15))
    root.mainloop()

#Abre uma janela para o usuário selecionar um arquivo CSV do SIGAA, armazena o caminho do arquivo selecionado 
#na variável global ARQ_SIGAA e atualiza o texto do label_sigaa com o nome do arquivo escolhido.
def select_sigaa():
    global ARQ_SIGAA
    arquivo = filedialog.askopenfilename(title="Selecione o arquivo SIGAA", filetypes=[("CSV files", "*.csv")])
    if arquivo:
        ARQ_SIGAA = arquivo
        label_sigaa.config(text=os.path.basename(arquivo), fg="black")


#Abre uma janela para o usuário selecionar um arquivo CSV do SISTEC, armazena o caminho do arquivo selecionado 
#na variável global ARQ_SISTEC e atualiza o texto do label_sistec com o nome do arquivo escolhido.
def select_sistec():
    global ARQ_SISTEC
    arquivo = filedialog.askopenfilename(title="Selecione o arquivo SISTEC", filetypes=[("CSV files", "*.csv")])
    if arquivo:
        ARQ_SISTEC = arquivo
        label_sistec.config(text=os.path.basename(arquivo), fg="black")


start_interface()
