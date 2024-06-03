import os
import csv

def calculate_charge(smiles):
    # Função para calcular a carga líquida com base em '-' e '+'
    charge = smiles.count('+') - smiles.count('-')
    return charge

def generate_mop_files(mol2_directory, mop_directory, csv_file):
    # Verifica se o diretório de saída existe, caso contrário, cria-o
    if not os.path.exists(mop_directory):
        os.makedirs(mop_directory)

    # Lê o arquivo CSV com os códigos SMILES e outras informações
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Itera sobre os arquivos MOL2 no diretório especificado
        for i, mol2_file in enumerate(os.listdir(mol2_directory)):
            if mol2_file.endswith(".mol2"):
                mol2_path = os.path.join(mol2_directory, mol2_file)
                mop_file = mol2_file[:-5] + ".mop"
                mop_path = os.path.join(mop_directory, mop_file)

                # Obtém o código SMILES da linha atual do CSV (linha atual + 1 para ignorar o título)
                csv_row = next(csv_reader)
                smiles = csv_row['SMILES']

                charge = calculate_charge(smiles)

                # Gera o arquivo .mop a partir do arquivo MOL2 com a carga calculada
                convert_mol2_to_mop(mol2_path, mop_path, charge)

def convert_mol2_to_mop(mol2_path, mop_path, charge):
    # Abre o arquivo MOL2 para leitura
    with open(mol2_path, 'r') as mol2_file:
        # Lê as linhas do arquivo MOL2
        mol2_lines = mol2_file.readlines()[7:]  # Ignora as primeiras 7 linhas

    # Encontra o índice onde a string "@<TRIPOS>BOND" aparece
    end_index = next((i for i, line in enumerate(mol2_lines) if "@<TRIPOS>BOND" in line), None)

    # Se encontrou a string, remove as linhas a partir desse índice
    if end_index is not None:
        mol2_lines = mol2_lines[:end_index]

    # Abre o arquivo .mop para escrita
    with open(mop_path, 'w') as mop_file:
        # Escreve as palavras-chave no arquivo .mop, incluindo a carga calculada
        mop_file.write(f" AUX LARGE CHARGE=0 SINGLET PREC PM3 T=3600 CAMP XYZ NOINTER SCALE=1.4 NSURF=2 SCINCR=0.4 NOMM GRAPH SYBYL NOOPT CHARGE={charge}\ncarga\n\n")

        # Escreve as linhas convertidas do arquivo MOL2 no arquivo .mop
        for line in mol2_lines:
            # Escreve a linha do arquivo MOL2 no arquivo .mop
            mop_file.write(line)

# Diretório contendo os arquivos MOL2 de entrada
mol2_directory = "C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1_G1/MOPAC_2cargas"

# Diretório de saída para os arquivos MOP
mop_directory = "C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1_G1/MOPAC_2cargas"

# Arquivo CSV com os códigos SMILES e outras informações
csv_file = "C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1_G1/1G1.csv"  # Substitua pelo caminho correto

# Gera os arquivos .mop a partir dos arquivos MOL2 com as cargas calculadas apropriadas
generate_mop_files(mol2_directory, mop_directory, csv_file)
