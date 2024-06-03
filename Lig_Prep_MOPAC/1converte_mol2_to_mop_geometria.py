import os

def generate_mop_files(mol2_directory, mop_directory):
    # Verifica se o diretório de saída existe, caso contrário, cria-o
    if not os.path.exists(mop_directory):
        os.makedirs(mop_directory)

    # Percorre todos os arquivos MOL2 no diretório especificado
    for mol2_file in os.listdir(mol2_directory):
        if mol2_file.endswith(".mol2"):
            mol2_path = os.path.join(mol2_directory, mol2_file)
            mop_file = mol2_file[:-5] + ".mop"
            mop_path = os.path.join(mop_directory, mop_file)

            # Gera o arquivo .mop a partir do arquivo MOL2
            convert_mol2_to_mop(mol2_path, mop_path)

def convert_mol2_to_mop(mol2_path, mop_path):
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
        # Escreve as palavras-chave no arquivo .mop
        mop_file.write("  AUX LARGE PREC PM3 T=3600 XYZ OPT SYBYL\ngeometria\n\n")

        # Escreve as linhas convertidas do arquivo MOL2 no arquivo .mop
        for i, line in enumerate(mol2_lines):
            # Divide a linha em campos
            fields = line.split()

            # Extrai as informações do átomo da linha do MOL2
            atom_name = fields[1]
            x_coord = float(fields[2])
            y_coord = float(fields[3])
            z_coord = float(fields[4])

            # Escreve a linha no formato desejado no arquivo .mop
            mop_file.write(f"{atom_name:>6}{x_coord:>10.4f}      1  {y_coord:>10.4f}      1  {z_coord:>10.4f}     1\n")

# Diretório contendo os arquivos MOL2 de entrada
mol2_directory = "C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1_G1/mol2"

# Diretório de saída para os arquivos MOP
mop_directory = "C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1_G1/MOPAC_1geometria"

# Gera os arquivos .mop a partir dos arquivos MOL2
generate_mop_files(mol2_directory, mop_directory)
