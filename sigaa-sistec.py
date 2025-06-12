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
        'Curso': s.get('NO_CICLO_MATRICULA', ''),
        'Origem': 'SISTEC'
    } for s in sistec if CPF_to_int(s['NU_CPF']) in diff_sistec]
    
    apenas_sigaa = [{
        'CPF': sg['CPF'],
        'Nome': sg.get('Nome', ''),
        'Curso': sg.get('Curso', ''),
        'Origem': 'SIGAA'
    } for sg in sigaa if CPF_to_int(sg['CPF']) in diff_sigaa]
    
    return apenas_sistec, apenas_sigaa

def find_differences_with_course_check(sistec, sigaa):
    cpfs_sistec_map = {CPF_to_int(s['NU_CPF']): s for s in sistec if CPF_to_int(s['NU_CPF']) is not None}
    cpfs_sigaa_map = {CPF_to_int(sg['CPF']): sg for sg in sigaa if CPF_to_int(sg['CPF']) is not None}

    cpfs_sistec_set = set(cpfs_sistec_map.keys())
    cpfs_sigaa_set = set(cpfs_sigaa_map.keys())

    # CPFs únicos em cada sistema (lógica original)
    diff_sistec_only = cpfs_sistec_set - cpfs_sigaa_set
    diff_sigaa_only = cpfs_sigaa_set - cpfs_sistec_set

    # CPFs presentes em ambos os sistemas
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

    # Nova seção para diferenças de curso
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
    """
    Cria um arquivo CSV a partir de uma lista de dicionários.

    Args:
        data (list of dict): Uma lista de dicionários, onde cada dicionário
                             representa uma linha do CSV e as chaves são os nomes das colunas.
        filename (str): O nome do arquivo CSV a ser criado (ex: 'meu_arquivo.csv').
    """
    if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        print("❌ Erro: 'data' deve ser uma lista de dicionários.")
        return

    if not data:
        print(f"⚠️ Atenção: A lista de dados está vazia. O arquivo '{filename}' será criado, mas estará vazio.")
        df = pd.DataFrame() # Cria um DataFrame vazio
    else:
        df = pd.DataFrame(data)

    df.to_csv(filename, index=False, encoding='utf-8') # Adicionado encoding para melhor compatibilidade
    print(f"✅ Arquivo '{filename}' criado com sucesso!")

# Cria pasta se não existir
os.makedirs(PASTA_ARQUIVOS, exist_ok=True)

# Processamento
print("🔍 Processando dados...")
sistec_filtrado = filter(df_sistec, col_sistec, 23, 'EM_CURSO')  # Ajuste o índice 23 conforme necessário
sigaa_filtrado = df_sigaa  # Você pode adicionar filtros para o SIGAA se necessário

lista_sistec = ToList(sistec_filtrado)
lista_sigaa = ToList(sigaa_filtrado)

# apenas_sistec, apenas_sigaa = find_differences(lista_sistec, lista_sigaa)
apenas_sistec, apenas_sigaa, diferencas_curso = find_differences_with_course_check(lista_sistec, lista_sigaa)
# Resultados
print(f"👥 Alunos apenas no SISTEC: {len(apenas_sistec)}")
print(f"👥 Alunos apenas no SIGAA: {len(apenas_sigaa)}")
print(f"📚 Diferenças de curso: {len(diferencas_curso)}")
# Gerando os arquivos
makeCSV(apenas_sistec, ARQ_SAIDA_SISTEC)
makeCSV(apenas_sigaa, ARQ_SAIDA_SIGAA)
makeCSV(diferencas_curso, os.path.join(PASTA_ARQUIVOS, 'diferencas_curso.csv'))

input("✅ Processo concluído. Pressione Enter para sair...")