import os

def separate_protein_ligand(input_pdb_file, protein_output_file, ligand_output_file):
    with open(input_pdb_file, 'r') as pdb_file:
        pdb_lines = pdb_file.readlines()

    protein_lines = []
    ligand_lines = []
    is_ligand = False

    for line in pdb_lines:
        if line.startswith('HETATM'):
            res_name = line[17:20].strip()
            if '***' in line or 'UNK' in line:
                is_ligand = True
            elif res_name == 'HOH':
                is_ligand = False

        if is_ligand:
            ligand_lines.append(line)
        else:
            protein_lines.append(line)

    with open(protein_output_file, 'w') as protein_file:
        protein_file.writelines(protein_lines)

    with open(ligand_output_file, 'w') as ligand_file:
        ligand_file.writelines(ligand_lines)


def process_pdb_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdb"):
                input_pdb_file = os.path.join(root, file)
                protein_output_file = os.path.join(root, "receptor.pdb")
                ligand_output_file = os.path.join(root, "ligand.pdb")
                separate_protein_ligand(input_pdb_file, protein_output_file, ligand_output_file)


if __name__ == "__main__":
    results_directory = r"C:/Users/Portilho/Desktop/Docking_certo/Resultados/Results_Docking/4AGS/sitio_2/Metabolitos"
    process_pdb_files_in_directory(results_directory)
