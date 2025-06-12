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
ARQ_SAIDA_SISTEC = os.path.join(PASTA_ARQUIVOS, 'apenas_no_sistec.csv')
ARQ_SAIDA_SIGAA = os.path.join(PASTA_ARQUIVOS, 'apenas_no_sigaa.csv')

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
    return df[df[col[col_n]].astype(str).str.contains(filtro, na=False)]

def ToList(df):
    return [dict(row) for _, row in df.iterrows()]

def find_differences(sistec, sigaa):
    # Converte CPFs para inteiros e remove duplicatas
    cpfs_sistec = {CPF_to_int(s['NU_CPF']) for s in sistec if CPF_to_int(s['NU_CPF']) is not None}
    cpfs_sigaa = {CPF_to_int(sg['CPF']) for sg in sigaa if CPF_to_int(sg['CPF']) is not None}
    
    # Encontra diferenças
    diff_sistec = cpfs_sistec - cpfs_sigaa
    diff_sigaa = cpfs_sigaa - cpfs_sistec
    
    # Formata os resultados
    apenas_sistec = [{
        'CPF': s['NU_CPF'],
        'Nome': s['NO_ALUNO'],
        'Situação': s.get('NO_STATUS_MATRICULA', ''),
        'Origem': 'SISTEC'
    } for s in sistec if CPF_to_int(s['NU_CPF']) in diff_sistec]
    
    apenas_sigaa = [{
        'CPF': sg['CPF'],
        'Nome': sg.get('Nome', ''),
        'Curso': sg.get('Curso', ''),
        'Origem': 'SIGAA'
    } for sg in sigaa if CPF_to_int(sg['CPF']) in diff_sigaa]
    
    return apenas_sistec, apenas_sigaa

def makeCSV(data, filename):
    df = pd.DataFrame(data)
    # Ordena as colunas de forma consistente
    colunas_ordenadas = ['CPF', 'Nome', 'Curso', 'Situação', 'Origem']
    # Seleciona apenas as colunas que existem nos dados
    colunas_existentes = [col for col in colunas_ordenadas if col in df.columns]
    df = df[colunas_existentes]
    df.to_csv(filename, index=False)
    print(f"✅ Arquivo '{filename}' criado com sucesso!")

# Cria pasta se não existir
os.makedirs(PASTA_ARQUIVOS, exist_ok=True)

# Processamento
print("🔍 Processando dados...")
sistec_filtrado = filter(df_sistec, col_sistec, 23, 'EM_CURSO')  # Ajuste o índice 23 conforme necessário
sigaa_filtrado = df_sigaa  # Você pode adicionar filtros para o SIGAA se necessário

lista_sistec = ToList(sistec_filtrado)
lista_sigaa = ToList(sigaa_filtrado)

apenas_sistec, apenas_sigaa = find_differences(lista_sistec, lista_sigaa)

# Resultados
print(f"👥 Alunos apenas no SISTEC: {len(apenas_sistec)}")
print(f"👥 Alunos apenas no SIGAA: {len(apenas_sigaa)}")

# Gerando os arquivos
makeCSV(apenas_sistec, ARQ_SAIDA_SISTEC)
makeCSV(apenas_sigaa, ARQ_SAIDA_SIGAA)

input("✅ Processo concluído. Pressione Enter para sair...")