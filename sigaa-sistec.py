import os
import subprocess
import sys

# Garante que o script usa o diretório onde ele está salvo
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Instala pandas se necessário
def install_pandas():
    try:
        import pandas as pd
    except ImportError:
        print("Instalando pandas...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        import pandas as pd
    print("✅ Pandas instalado com sucesso!")
    print("📦 Versão do pandas:", pd.__version__)

install_pandas()
import pandas as pd

# Caminhos dos arquivos
PASTA_ARQUIVOS = 'CSVs'
ARQ_SISTEC = os.path.join(PASTA_ARQUIVOS, 'sistec.csv')
ARQ_SIGAA = os.path.join(PASTA_ARQUIVOS, 'sigaa.csv')
ARQ_SAIDA = os.path.join(PASTA_ARQUIVOS, 'sistec-sigaa.csv')

# Verifica se os arquivos de entrada existem
if not os.path.exists(ARQ_SISTEC):
    print(f"❌ Arquivo '{ARQ_SISTEC}' não encontrado. Por favor, coloque o arquivo na pasta '{PASTA_ARQUIVOS}' e rode novamente.")
    input("Pressione Enter para sair...")
    sys.exit(1)

if not os.path.exists(ARQ_SIGAA):
    print(f"❌ Arquivo '{ARQ_SIGAA}' não encontrado. Por favor, coloque o arquivo na pasta '{PASTA_ARQUIVOS}' e rode novamente.")
    input("Pressione Enter para sair...")
    sys.exit(1)

# Lê os arquivos
df_sistec = pd.read_csv(ARQ_SISTEC, sep=',')
df_sigaa = pd.read_csv(ARQ_SIGAA, sep=',')

col_sistec = df_sistec.columns.tolist()
col_sigaa = df_sigaa.columns.tolist()

# Funções auxiliares
def CPF_to_int(cpf):
    try:
        return int(str(cpf).replace('.', '').replace('-', '').split('.')[0])
    except Exception:
        return None

def filter(df, col, col_n, filtro):
    filtered = df[df[col[col_n]].astype(str).str.contains(filtro, na=False)]
    return [dict(row) for _, row in filtered.iterrows()]

def ToList(df, col):
    return [dict(row) for _, row in df.iterrows()]

def cross_Cpf(sistec, sigaa):
    resultado = []
    for s in sistec:
        cpf_s = CPF_to_int(s.get('NU_CPF'))
        if cpf_s is None:
            continue
        for sg in sigaa:
            cpf_sigaa = CPF_to_int(sg.get('CPF'))
            if cpf_sigaa is None:
                continue
            if cpf_s == cpf_sigaa:
                resultado.append({
                    'CPF': s['NU_CPF'],
                    'Nome': s['NO_ALUNO'],
                    'Curso': sg.get('Curso'),
                    'Situação': s.get('NO_STATUS_MATRICULA')
                })
    return resultado

def makeCSV(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Arquivo '{filename}' criado com sucesso!")

# Cria pasta se não existir
os.makedirs(PASTA_ARQUIVOS, exist_ok=True)

# Processamento
print("🔍 Processando dados...")
sistec_filtrado = filter(df_sistec, col_sistec, 23, 'EM_CURSO')
sigaa_lista = ToList(df_sigaa, col_sigaa)
resultado = cross_Cpf(sistec_filtrado, sigaa_lista)

# Resultado
print(f"👥 Alunos encontrados no cruzamento: {len(resultado)}")
makeCSV(resultado, ARQ_SAIDA)

input("✅ Processo concluído. Pressione Enter para sair...")
